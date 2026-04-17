#ifdef _WIN32
#define API __declspec(dllexport)
#else
#define API
#endif

#include "matrix.h"

int32_t roll_l_func(uint32_t number, uint32_t offset) {
  if (offset >= 32)
    offset %= 32;
  return (number >> (32 - offset)) | (number << offset);
}

uint32_t roll_r_func(uint32_t number, uint32_t offset) {
  if (offset >= 32)
    offset %= 32;
  return (number << (32 - offset)) | (number >> offset);
}

API void process(uint32_t *arr, uint32_t *out, Matrix mantis, uint32_t start,
                 uint32_t length, uint32_t salt) {
  if (length == 0)
    return;

  uint32_t left = 1;

  for (uint32_t i = start; i < start + length; i++) {
    uint32_t subject = i ^ arr[i];

    for (int r = 0; r < 20; r++) {
      uint32_t row = subject & 0xF;
      uint32_t col = (subject >> 4) & 0xF;

      uint32_t off = (salt * (row + col) + 1) & 0x2F;

      subject = (collect(&mantis, row, col) ^ subject) * mantis.constant;

      uint32_t rol = ~(row ^ col) * salt + 1;

      write(&mantis, row, col, subject);

      subject = left == 1 ? roll_l_func(subject, row * off)
                          : roll_r_func(subject, row * off);

      left ^= 1;
    }
  }

  for (int i = 0; i < 32; i++) {
    out[i] = collect_inclusive_disjunction_column(&mantis, i) ^ salt;
  }
}
