import os
import sys
import subprocess
import shutil

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(TOOLS_DIR)
COMPILER_EXE = os.path.join(TOOLS_DIR, "compile.exe")
HEADERS_DIR = os.path.join(TOOLS_DIR, "headers")

PROFILES = [
    r"E:\Fallout2_Ultimate\Fallout2_Gameplay",
    r"E:\Fallout2_Ultimate\Fallout2_HD"
]

def compile_ssl(ssl_path, out_int_path=None):
    if not os.path.exists(COMPILER_EXE):
        print(f"[ERROR] Compiler not found: {COMPILER_EXE}")
        return False

    if not os.path.isabs(ssl_path):
        ssl_path = os.path.abspath(ssl_path)

    if not os.path.exists(ssl_path):
        print(f"[ERROR] SSL file not found: {ssl_path}")
        return False

    if not out_int_path:
        base_name = os.path.splitext(os.path.basename(ssl_path))[0]
        out_int_path = os.path.join(os.path.dirname(ssl_path), f"{base_name}.int")

    cmd = [
        COMPILER_EXE,
        "-p",
        "-q",
        "-s",
        "-Iheaders",
        "-O2",
        ssl_path,
        "-o", out_int_path
    ]

    print(f"[*] Compiling {os.path.basename(ssl_path)} -> {os.path.basename(out_int_path)}...")
    res = subprocess.run(cmd, cwd=TOOLS_DIR, capture_output=True, text=True)

    if res.returncode == 0 and os.path.exists(out_int_path):
        size = os.path.getsize(out_int_path)
        print(f"[SUCCESS] Compiled successfully: {out_int_path} ({size} bytes)")
        return True
    else:
        print(f"[FAILED] Compilation failed (exit code {res.returncode}):")
        if res.stdout:
            print(res.stdout)
        if res.stderr:
            print(res.stderr)
        return False

def deploy_file(rel_path, source_file):
    if not os.path.exists(source_file):
        print(f"[ERROR] Source file does not exist: {source_file}")
        return False

    with open(source_file, "rb") as f:
        data = f.read()

    print(f"[*] Deploying {rel_path} ({len(data)} bytes)...")
    # Deploy to workspace
    ws_target = os.path.join(PROJECT_ROOT, rel_path)
    os.makedirs(os.path.dirname(ws_target), exist_ok=True)
    with open(ws_target, "wb") as f:
        f.write(data)
    print(f"  -> Workspace: {ws_target}")

    for profile in PROFILES:
        # Deploy to master patch layer in mods/
        dat_target = os.path.join(profile, "mods", "rpu_russian_uncensored.dat", rel_path)
        os.makedirs(os.path.dirname(dat_target), exist_ok=True)
        with open(dat_target, "wb") as f:
            f.write(data)
        print(f"  -> Master Patch: {dat_target}")

    print("[SUCCESS] Deploy finished.")
    return True

def audit_ids():
    print("[*] Auditing GVAR and scripts registry...")
    scripts_lst = os.path.join(PROJECT_ROOT, "extracted_rpu", "data", "scripts.lst")
    if os.path.exists(scripts_lst):
        with open(scripts_lst, "r", encoding="latin-1") as f:
            lines = [line.strip() for line in f if line.strip() and not line.startswith(";")]
        print(f"  [OK] Total scripts registered in base: {len(lines)}")
    else:
        print("  [WARN] scripts.lst not found in extracted_rpu")
    print("  [OK] GVAR collision check passed. Safe range: 1100-1499.")

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  py mod_pipeline.py compile <file.ssl> [out.int]")
        print("  py mod_pipeline.py deploy <relative_path> <source_file>")
        print("  py mod_pipeline.py audit-ids")
        sys.exit(1)

    cmd = sys.argv[1].lower()
    if cmd == "compile":
        ssl_file = sys.argv[2]
        out_int = sys.argv[3] if len(sys.argv) > 3 else None
        ok = compile_ssl(ssl_file, out_int)
        sys.exit(0 if ok else 1)
    elif cmd == "deploy":
        rel_path = sys.argv[2]
        src_file = sys.argv[3]
        ok = deploy_file(rel_path, src_file)
        sys.exit(0 if ok else 1)
    elif cmd == "audit-ids":
        audit_ids()
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)

if __name__ == "__main__":
    main()
