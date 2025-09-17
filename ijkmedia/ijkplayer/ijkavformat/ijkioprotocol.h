/*
 * Copyright (c) 2016 Bilibili
 * Copyright (c) 2016 Raymond Zheng <raymondzheng1412@gmail.com>
 *
 * This file is part of ijkPlayer.
 *
 * ijkPlayer is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * ijkPlayer is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with ijkPlayer; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
 */
#include "ijkiourl.h"

int ijkio_alloc_url(IjkURLContext **inner, const char *url);
int ijkio_url_alloc(IjkURLContext **inner, const char *url, int flags, void *interrupt_cb);
int ijkio_url_read(IjkURLContext *h, unsigned char *buf, int size);
int64_t ijkio_url_seek(IjkURLContext *h, int64_t pos, int whence);
int ijkio_url_close(IjkURLContext *h);
