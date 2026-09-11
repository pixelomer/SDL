#!/usr/bin/env python3
"""Build the static SDL2 Horizon port without modifying the installed SDK."""
import argparse, hashlib, json, os, subprocess
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--output',type=Path,required=True); p.add_argument('--libnx',type=Path,required=True)
a=p.parse_args(); out=a.output.resolve(); sdk=a.libnx.resolve()
if out.exists(): p.error('Choose a new output directory')
if not (sdk/'switch.specs').is_file(): p.error('Missing libnx SDK')
source=Path(__file__).resolve().parents[1]; dkp=Path(os.environ.get('DEVKITPRO','/opt/devkitpro'))
out.mkdir(parents=True)
toolchain=out/'Switch.cmake'; toolchain.write_text('include("'+str(dkp/'cmake/Switch.cmake')+'")\nset(NX_ROOT "'+str(sdk)+'")\nlist(PREPEND CMAKE_FIND_ROOT_PATH "'+str(sdk)+'")\n')
commands=[['cmake','-S',str(source),'-B',str(out),'-G','Ninja','-DCMAKE_TOOLCHAIN_FILE='+str(toolchain),'-DCMAKE_POLICY_VERSION_MINIMUM=3.5',
    '-DCMAKE_BUILD_TYPE=RelWithDebInfo','-DSDL_SHARED=OFF','-DSDL_STATIC=ON','-DSDL_TEST=OFF','-DSDL_TESTS=OFF','-DSDL_POWER=OFF','-DSDL_FILESYSTEM=OFF','-DSDL_CPUINFO=ON','-DSDL_PTHREADS=ON'],
    ['cmake','--build',str(out),'--parallel','8']]
for command in commands: subprocess.run(command,check=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest={'revision':subprocess.check_output(['git','rev-parse','HEAD'],cwd=source,text=True).strip(),'commands':commands,
    'libnx_archive_sha256':sha(sdk/'lib/libnx.a'),'archive_sha256':sha(out/'libSDL2.a'),
    'source_sha256':{str(p.relative_to(source)):sha(p) for p in [Path(__file__),source/'src/video/switch/SDL_switchvideo.c']}}
(out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
(out/'source-diff.patch').write_bytes(subprocess.check_output(['git','diff','--binary'],cwd=source))
