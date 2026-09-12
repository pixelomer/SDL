/*
  Simple DirectMedia Layer
  Copyright (C) 1997-2020 Sam Lantinga <slouken@libsdl.org>

  This software is provided 'as-is', without any express or implied
  warranty.  In no event will the authors be held liable for any damages
  arising from the use of this software.

  Permission is granted to anyone to use this software for any purpose,
  including commercial applications, and to alter it and redistribute it
  freely, subject to the following restrictions:

  1. The origin of this software must not be misrepresented; you must not
     claim that you wrote the original software. If you use this software
     in a product, an acknowledgment in the product documentation would be
     appreciated but is not required.
  2. Altered source versions must be plainly marked as such, and must not be
     misrepresented as being the original software.
  3. This notice may not be removed or altered from any source distribution.
*/
#include "../../SDL_internal.h"

#ifdef SDL_FILESYSTEM_SWITCH

/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
/* System dependent filesystem routines                                */

#include <limits.h>
#include <fcntl.h>
#include <sys/unistd.h>

#include "SDL_error.h"
#include "SDL_stdinc.h"
#include "SDL_filesystem.h"

char *
SDL_GetBasePath(void)
{
    const char *basepath = "romfs:/";
    char *retval = SDL_strdup(basepath);
    return retval;
}

char *
SDL_GetPrefPath(const char *org, const char *app)
{
    /* Altered for the managed homebrew host. Keep the upstream current-directory
       policy; applications must select their private working directory first.
       An absolute path on the default SD mount also works in CLR path APIs,
       which otherwise interpret the native "sdmc:" prefix as a relative path. */
    char buf[PATH_MAX + 1];
    const char *path;
    char *ret;
    size_t len;
    if (!getcwd(buf, sizeof(buf))) {
        SDL_SetError("Could not obtain the Switch working directory");
        return NULL;
    }
    path = SDL_strncmp(buf, "sdmc:/", 6) == 0 ? buf + 5 : buf;
    len = SDL_strlen(path);
    ret = SDL_malloc(len + 2);
    if (!ret) {
        SDL_OutOfMemory();
        return NULL;
    }
    SDL_memcpy(ret, path, len);
    if (len == 0 || path[len - 1] != '/') ret[len++] = '/';
    ret[len] = '\0';
    return ret;
}

#endif /* SDL_FILESYSTEM_SWITCH */

/* vi: set ts=4 sw=4 expandtab: */
