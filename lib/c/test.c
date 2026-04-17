#include "processor.h"
#include <stdio.h>

int main() {
  uint32_t nums[2] = {0, 1};
  uint32_t salt = 1;

  uint32_t out[32] = {0};

  Matrix mantis;

  fill(&mantis, nums, 2);

  process(nums, out, mantis, 0, 2, salt);

  for (int i = 0; i < 32; i++) {
    printf("%d\n", out[i]);
  }

  return 0;
}
