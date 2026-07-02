// ---------------------------------------------------------------------------
// File: allocator.cc
// Note: Copyright (c) 2026 by Jens Kallup - paule32
//       all rights reserved.
// ---------------------------------------------------------------------------
# include "stddef.h"
# include "allocator.h"

namespace std {
    
template<typename T>
T* Allocator<T>::alloc(uint32_t count) {
    return (T*)_jit_malloc(sizeof(T) * count);
}

template<typename T>
T* Allocator<T>::realloc(T* p, uint32_t count) {
    return (T*)_jit_realloc(p, sizeof(T) * count);
}

template<typename T>
void Allocator<T>::free(T* p) {
    _jit_free(p);
}

template struct Allocator<char>;
template struct Allocator<int>;
template struct Allocator<double>;

}   // namespace: std
