#!/usr/bin/env python3
"""Fetch dependencies and cross-build the static Horizon library."""
import argparse, json, os, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'eng/horizon'))
from support import digest, libnx, read_mirrors, run, submodules, switch_toolchain
p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--output', type=Path, default=ROOT / 'artifacts/horizon')
p.add_argument('--libnx', type=Path, help='Optional prebuilt libnx SDK override')
p.add_argument('--jobs', type=int, default=min(os.cpu_count() or 2, 8))
p.add_argument('--source-mirrors', type=Path)
a = p.parse_args()
if a.jobs < 1: p.error('--jobs must be positive')
mirrors = read_mirrors(a.source_mirrors)
submodules(ROOT, mirrors)
spec = json.loads((ROOT / 'eng/horizon/dependencies.json').read_text())
sdk = libnx(ROOT, spec['libnx'], mirrors, a.jobs, a.libnx)
out = a.output.resolve()
toolchain = switch_toolchain(out, sdk)
port = Path(os.environ.get('DEVKITPRO', '/opt/devkitpro')) / 'portlibs/switch'
options = ['-DSDL_SHARED=OFF', '-DSDL_STATIC=ON', '-DSDL_TEST=OFF', '-DSDL_TESTS=OFF', '-DSDL_POWER=OFF', '-DSDL_FILESYSTEM=ON', '-DSDL_CPUINFO=ON', '-DSDL_PTHREADS=ON']
if 'SDL' == 'FNA3D':
    options += ['-DSDL2_INCLUDE_DIRS=' + str(port / 'include/SDL2'), '-DSDL2_LIBRARIES=' + str(port / 'lib/libSDL2.a')]
run(['cmake', '-S', ROOT, '-B', out, '-G', 'Ninja', '-DCMAKE_TOOLCHAIN_FILE=' + str(toolchain),
     '-DCMAKE_POLICY_VERSION_MINIMUM=3.5', '-DCMAKE_BUILD_TYPE=RelWithDebInfo', *options])
run(['cmake', '--build', out, '--parallel', a.jobs, '--target', *['SDL2-static']])
manifest = {'revision': subprocess.check_output(['git', '-C', ROOT, 'rev-parse', 'HEAD'], text=True).strip(),
            'libnx': str(sdk), 'libnx_archive_sha256': digest(sdk / 'lib/libnx.a'),
            'archives': {name: digest(out / name) for name in ['libSDL2.a']}}
if 'SDL' == 'SDL': manifest['archive_sha256'] = digest(out / 'libSDL2.a')
(out / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
print(out)
