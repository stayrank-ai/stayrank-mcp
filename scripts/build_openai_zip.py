#!/usr/bin/env python3
"""Valide puis zippe un paquet de plugin OpenAI (format Agent Plugins).
Usage: python build_openai_zip.py <dossier_plugin> <sortie.zip>
Regles: developers.openai.com/plugins/deploy/submission(.md) et /submission-errors(.md), lues le 2026-10-03.
Code retour 0 = aucune erreur (zip ecrit) ; 1 = au moins une erreur (rien n'est ecrit)."""
import json, os, re, struct, sys, zipfile

SCHEMA_PLUGIN = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
SCHEMA_MCP = "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"
CATS = {"Productivity", "Creativity", "Developer Tools", "Business & Operations", "Data & Analytics", "Communication",
        "Education & Research", "Security", "Finance", "Healthcare", "Travel", "Entertainment", "Other"}
TOP_KEYS = {"$schema", "name", "version", "description", "author", "homepage", "repository", "license", "keywords", "extensions"}
errs, warns = [], []


def E(code, msg):
    errs.append("ERREUR  %s: %s" % (code, msg))


def W(code, msg):
    warns.append("AVERT.  %s: %s" % (code, msg))


def https(u):
    return isinstance(u, str) and re.match(r"^https://[^/\s@]+[^\s]*$", u) is not None and len(u) <= 1024


def oneline(s):
    return isinstance(s, str) and s.strip() != "" and "\n" not in s and "\r" not in s


def png_size(p):
    with open(p, "rb") as f:
        h = f.read(24)
    if h[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">II", h[16:24])


def check_image(root, rel, field):
    if not isinstance(rel, str) or not rel.startswith("./"):
        return E("branding_asset_path_missing_root_prefix", "%s doit commencer par ./" % field)
    p = os.path.normpath(os.path.join(root, rel))
    if not p.startswith(os.path.normpath(root)):
        return E("declared_asset_path_outside_package", field)
    if not os.path.isfile(p):
        return E("declared_asset_file_missing", "%s -> %s" % (field, rel))
    ext = os.path.splitext(p)[1].lower()
    if ext not in (".png", ".jpg", ".jpeg", ".webp", ".svg"):
        return E("image_file_format_unsupported", rel)
    if os.path.getsize(p) > 5 * 1024 * 1024:
        E("image_file_too_large", rel)
    if ext == ".png":
        s = png_size(p)
        if not s:
            return E("raster_image_extension_content_mismatch", "%s n'est pas un vrai PNG" % rel)
        if s[0] != s[1]:
            E("raster_image_not_square", "%s %s" % (rel, s))
        if min(s) < 48:
            E("raster_image_dimensions_too_small", "%s %s" % (rel, s))
        if max(s) > 4096:
            E("raster_image_dimensions_too_large", "%s %s" % (rel, s))
    else:
        W("manuel", "%s: verifier a la main carre, >=48, <=4096" % rel)


def main(root, out):
    root = os.path.abspath(root)
    mp = os.path.join(root, "plugin.json")
    if not os.path.isfile(mp):
        return E("plugin_manifest_missing", "plugin.json absent a la racine")
    try:
        m = json.load(open(mp, encoding="utf-8"))
    except Exception as e:
        return E("plugin_manifest_json_malformed", str(e))
    if not isinstance(m, dict):
        return E("plugin_manifest_root_not_object", "")
    if m.get("$schema") != SCHEMA_PLUGIN:
        E("schema", "$schema doit valoir %s" % SCHEMA_PLUGIN)
    for k in m:
        if k not in TOP_KEYS:
            E("schema_closed", "cle racine inconnue '%s' (schema ferme)" % k)
    n = m.get("name")
    if not isinstance(n, str) or not re.fullmatch(r"[a-z0-9](?:[a-z0-9-]*[a-z0-9])?", n) or "--" in n or len(n) > 64:
        E("plugin_name_format", "name: minuscules/chiffres/tirets, <=64, sans '--'")
        n = n if isinstance(n, str) else ""
    if not re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?", str(m.get("version", ""))):
        E("plugin_version_not_semver", "version semver requise")
    d = m.get("description")
    if not isinstance(d, str) or not d.strip():
        E("plugin_description_missing", "")
    elif len(d) > 1024:
        E("plugin_description_too_long", "%d > 1024 (limite de validation du paquet)" % len(d))
    a = m.get("author")
    if not isinstance(a, dict) or not oneline(a.get("name")) or len(a["name"]) > 120:
        E("plugin_developer_missing", "author.name requis (<=120)")
    elif set(a) - {"name", "email", "url"}:
        E("schema_closed", "author n'accepte que name/email/url")
    elif "url" in a and not (isinstance(a["url"], str) and a["url"].startswith("https://")):
        E("plugin_author_url_not_https", "")
    if "homepage" in m and not (isinstance(m["homepage"], str) and m["homepage"].startswith("https://")):
        E("plugin_homepage_format", "")
    ox = (m.get("extensions") or {}).get("com.openai")
    if not isinstance(ox, dict):
        E("extensions", "extensions.com.openai requis (objet)")
        ox = {}
    for k in ox:
        if k not in {"interface", "onboardingSkill", "review", "publication", "id"}:
            E("champ_openai", "extensions.com.openai.%s non prevu pour une soumission (apps/hooks interdits)" % k)
    i = ox.get("interface") or {}
    for k, lim in (("displayName", 30), ("shortDescription", 30), ("developerName", 80)):
        v = i.get(k)
        if not oneline(v):
            E("interface." + k, "requis, une ligne")
        elif len(v) > lim:
            E("interface." + k, "%d > %d" % (len(v), lim))
    ld = i.get("longDescription")
    if not isinstance(ld, str) or not ld.strip() or len(ld) > 4000:
        E("interface.longDescription", "requis, <=4000")
    if i.get("category") not in CATS:
        E("plugin_category_unknown", "%r hors liste" % i.get("category"))
    caps = i.get("capabilities", [])
    if not isinstance(caps, list) or len(caps) > 20 or any((not oneline(c)) or len(c) > 120 for c in caps):
        E("plugin_capabilities", "<=20 entrees, <=120 car., une ligne")
    for k in ("websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL"):
        if not https(i.get(k)):
            E("interface." + k, "HTTPS requis (<=1024) pour une soumission MCP")
    dp = i.get("defaultPrompt", [])
    dp = [dp] if isinstance(dp, str) else dp
    if len(dp) > 3 or len(set(x.strip().lower() for x in dp)) != len(dp) or any((not oneline(x)) or len(x) > 128 or "@" in x for x in dp):
        E("defaultPrompt", "<=3, uniques, <=128, une ligne, sans @mention")
    for k in ("brandColor", "brandColorDark"):
        if k in i and not re.fullmatch(r"#[0-9A-Fa-f]{6}", str(i[k])):
            E("plugin_brand_color_format", k)
    if i.get("screenshots"):
        W("screenshots", "a ne declarer que si l'UI existe: 1 PNG/JPEG par defaultPrompt, 706 px de large, 400-860 de haut (non verifie ici)")
    check_image(root, i.get("logo"), "interface.logo")
    check_image(root, i.get("composerIcon"), "interface.composerIcon")
    for k in ("logoDark", "composerIconDark"):
        if k in i:
            check_image(root, i[k], "interface." + k)
    sd = os.path.join(root, "skills")
    names = []
    if os.path.isdir(sd):
        for s in sorted(os.listdir(sd)):
            sp = os.path.join(sd, s, "SKILL.md")
            if s.startswith("."):
                E("skill_directory_hidden", s)
                continue
            if not os.path.isfile(sp):
                W("skill_file_ignored", "skills/%s sans SKILL.md" % s)
                continue
            t = open(sp, encoding="utf-8").read()
            mm = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n(.*)$", t, re.S)
            if not mm:
                E("skill_frontmatter_missing", s)
                continue
            fm = {}
            for line in mm.group(1).splitlines():
                if ":" in line and not line.startswith(" "):
                    k, v = line.split(":", 1)
                    fm[k.strip()] = v.strip().strip("'\"")
            if not fm.get("name"):
                E("skill_name_missing", s)
            if not fm.get("description"):
                E("skill_description_missing", s)
            elif len(fm["description"]) > 1024:
                E("skill_description_too_long", s)
            if not mm.group(2).strip():
                E("skill_body_empty", s)
            if len("%s:%s" % (n, fm.get("name", ""))) > 64:
                E("skill_identity_too_long", s)
            if re.search(r"claude|anthropic", t, re.I):
                W("skill_neutralite", "%s: mention de Claude/Anthropic (OpenAI demande un langage neutre)" % s)
            names.append(fm.get("name"))
        if len(names) != len(set(names)):
            E("skill_identity_duplicate", "")
    os_ = ox.get("onboardingSkill")
    if os_ and not os.path.isfile(os.path.join(root, os_[2:] if os_.startswith("./") else os_)):
        E("onboardingSkill", "doit pointer un SKILL.md inclus")
    mj = os.path.join(root, "mcp.json")
    if not os.path.isfile(mj):
        E("mcp", "mcp.json absent (requis pour une soumission MCP)")
    else:
        c = json.load(open(mj, encoding="utf-8"))
        if c.get("$schema") != SCHEMA_MCP or set(c) - {"$schema", "mcpServers"}:
            E("mcp_schema", "mcp.json: $schema + mcpServers uniquement")
        srv = c.get("mcpServers", {})
        if len(srv) != 1:
            E("mcp_server_count", "exactement 1 serveur MCP distant requis")
        for k, v in srv.items():
            if v.get("type") != "streamable-http" or set(v) - {"type", "url", "headers"}:
                E("mcp_server_wrong_type", "%s: type=streamable-http, cles type/url/headers" % k)
            if not str(v.get("url", "")).startswith("https://"):
                E("mcp_url", "%s: url https requise" % k)
            if "headers" in v:
                E("secret", "%s: aucun en-tete (visible par tous)" % k)
    for bad in (".app.json", ".mcp.json", ".claude-plugin", ".codex-plugin", "commands", "agents", "hooks", "hooks.json", "bin", "CLAUDE.md"):
        if os.path.exists(os.path.join(root, bad)):
            W("hors_format", "%s present: non prevu dans le paquet OpenAI recommande" % bad)
    rv = ox.get("review") or {}
    tc = rv.get("test_cases") or {}
    pos, neg = tc.get("positive", []), tc.get("negative", [])
    if len(pos) != 5 or len(neg) != 3:
        W("review", "%d positifs / %d negatifs (exige 5/3 avant soumission, pas pour l'upload)" % (len(pos), len(neg)))
    for x in pos:
        for k in ("description", "prompt", "tools_triggered", "expected_behavior"):
            if not x.get(k):
                E("review.positive", "champ %s manquant" % k)
    for x in neg:
        for k in ("description", "prompt"):
            if not x.get(k):
                E("review.negative", "champ %s manquant" % k)
    if not rv.get("demo_recording_url"):
        W("review", "demo_recording_url manquant (requis avant soumission)")
    if "test_credentials" in json.dumps(ox) or "reviewer_instructions" in json.dumps(ox):
        E("secret", "test_credentials/reviewer_instructions interdits dans le ZIP")
    files = []
    for dp_, dn, fn in os.walk(root):
        dn[:] = sorted(x for x in dn if x not in (".git", "node_modules"))
        for f in sorted(fn):
            full = os.path.join(dp_, f)
            rel = os.path.relpath(full, root).replace(os.sep, "/")
            if os.path.islink(full):
                E("archive_member_type_unsupported", rel)
            if f in (".DS_Store", "Thumbs.db") or f.endswith(".zip"):
                E("hygiene", "%s ne doit pas etre dans le paquet" % rel)
            if rel.count("/") + 1 > 20:
                E("archive_member_path_too_deep", rel)
            files.append((full, rel))
    if len(files) > 5000:
        E("archive_too_many_entries", str(len(files)))
    if errs:
        return
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for full, rel in sorted(files, key=lambda x: x[1]):
            zi = zipfile.ZipInfo(rel, date_time=(2026, 10, 3, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(full, "rb").read())
    sz = os.path.getsize(out)
    if sz > 100 * 1024 * 1024:
        E("archive_too_large", str(sz))
    print("OK: %s (%d octets, %d fichiers, plugin a la racine du zip)" % (out, sz, len(files)))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
    for l in warns + errs:
        print(l)
    sys.exit(1 if errs else 0)
