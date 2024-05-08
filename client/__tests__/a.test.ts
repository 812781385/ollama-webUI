import { expect, it } from 'vitest'

const sum2 = (a: number, b: number) => a + b
it('sum2(1,2)===3', () => {
  expect(sum2(1, 2)).toBe(3)
})
