import { expect, it } from 'vitest'

const sum1 = (a, b) => a + b
it('sum1(1,2)===3', () => {
  expect(sum1(1, 2)).toBe(3)
})
