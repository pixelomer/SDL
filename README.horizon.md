# SDL for Horizon

This SDL2 fork propagates Horizon focus state through SDL window events, prefers
the Switch video backend, and provides preference paths usable by managed hosts.
Applications select their libnx focus policy; SDL does not change it. Applications
that need notifications before HOME/sleep suspension can select
`SuspendHomeSleepNotify`. Focus updates use the state reported by libnx.
Upstream: [devkitPro/SDL](https://github.com/devkitPro/SDL), zlib license;
retain the upstream license and file notices. The port uses public devkitPro/libnx
homebrew interfaces. No Nintendo SDK is required.

## Build

On Linux, install Python 3.12+, Git, CMake, Ninja, make and devkitPro's switch-dev
and switch-portlibs packages. Set `DEVKITPRO` and put devkitA64/bin and tools/bin
on PATH. Build from any directory:

```sh
python3 build-horizon.py --jobs 8
```

The script fetches and builds pinned [libnx](https://github.com/pixelomer/libnx)
in ignored `artifacts/sources/`; it does not install over the system SDK.
`--libnx /path/to/sdk` optionally reuses a built SDK. Build outputs are under `artifacts/horizon/`. Keep symbols for application debugging.
Full commit pins are in `eng/horizon/dependencies.json` and Git submodule entries.
`--source-mirrors FILE.json` can map canonical URLs to local Git source mirrors;
mirrors supply source objects, never prebuilt libraries.

Archive output: `libSDL2.a`.
Use the paired [FNA](https://github.com/pixelomer/FNA) and
[FNA3D](https://github.com/pixelomer/FNA3D) revisions selected by the application.
These builds use SDL2/OpenGL and do not enable a Vulkan renderer.
