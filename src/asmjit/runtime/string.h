// ---------------------------------------------------------------------------
// File: string.h
// Note: Copyright (c) 2026 by Jens Kallup - paule32
//       all rights reserved.
// ---------------------------------------------------------------------------
#ifndef __DBASE2MANY_STRING_HH__
#define __DBASE2MANY_STRING_HH__

# pragma once
# include "stddef.h"

namespace std {
class string {
private:
    char* data_;
    unsigned int len_;
public:
     string();
     string(const char* s);
    ~string();

    const    char* c_str() const;
    unsigned int  length() const;
};
}

extern "C" {
DLL_API char * _jit_strdup(const char *s);
DLL_API size_t _jit_strlen(const char* str);

DLL_API char * _jit_strncpy(char *dest, const char *src, unsigned int count);
};

#endif
