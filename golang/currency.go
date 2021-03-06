package main

import (
	"math/big"
)

var (
	zero   = newCurrency("0.0")
	one    = newCurrency("1.0")
	two    = newCurrency("2.0")
	twenty = newCurrency("20.0")
	percent85 = newCurrency("0.85")
)

type currency struct {
	num *big.Rat
}

func newCurrency(num string) *currency {
	c := &currency{}
	c.num, _ = new(big.Rat).SetString(num)
	return c
}

func (c *currency) plus(o *currency) *currency {
	n := &currency{}
	n.num = new(big.Rat)
	n.num.Add(c.num, o.num)
	return n
}

func (c *currency) minus(o *currency) *currency {
	n := &currency{}
	n.num = new(big.Rat)
	n.num.Sub(c.num, o.num)
	return n
}

func (c *currency) mul(o *currency) *currency {
	n := &currency{}
	n.num = new(big.Rat)
	n.num.Mul(c.num, o.num)
	return n
}

func (c *currency) div(o *currency) *currency {
	n := &currency{}
	n.num = new(big.Rat)
	if o.num.Cmp(zero.num) != 0 {
		n.num.Quo(c.num, o.num)
	}
	return n
}

func (c *currency) moreThan(o *currency) bool {
	return c.num.Cmp(o.num) > 0
}

func (c *currency) str(precision int) string {
	return c.num.FloatString(precision)
}

func (c *currency) float() float64 {
	f, _ := c.num.Float64()
	return f
}

func percentChange(first, second float64) float64 {	
	abs := first - second
	if abs < 0 {
		abs = -abs	
	}
	return abs / second
}
