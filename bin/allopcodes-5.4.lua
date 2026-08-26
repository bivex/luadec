-- allopcodes-5.4.lua
local u1,u2,u3
function f1(a1,a2,...)
	local l0 = a1; -- move
	local l1 = 1 -- loadi
	local l2 = true -- loadtrue / loadfalse / lfalseskip
	local l3 = nil -- loadnil
	local l4 = u1[l3] -- gettabup
	u1[l3] = l4 -- settabup
	l1 = g1 -- gettabup l1 = _ENV["g1"]
	g1 = l1 -- settabup _ENV["g1"] = l1
	l2 = u2 -- getupval
	u2 = l2 -- setupval
	l1 = l3[l2] -- gettable
	l3[l2] = l1 -- settable
	local l5 = { -- newtable
		l1, l2; -- move, setlist
		x = l2 -- setfield
	}
	l5.x = 5 -- setfield
	local fv = l5.x -- getfield
	l5[1] = 10 -- seti
	local iv = l5[1] -- geti
	local l6 = l5:x() -- self, call
	local l7 = -((l0+l1-l2)*l3/l4%l5)^l6 -- add, sub, mul, div, mod, pow, unm, mmbin
	local l8 = #(not l7) -- not, len
	local l9 = l7..l8 -- concat
	local l10 = l0 + 5 -- addi, mmbini
	local l11 = l0 + 3.14 -- addk, mmbink
	local l12 = l0 >> 2 -- shri
	local l13 = 2 << l0 -- shli
	if l1==1 and l2<2 or l3<=3 or l4>4 or l5>=5 then -- eqi, lti, lei, gti, gei, jmp
		for i = 1, 10, 2 do -- forprep
			l0 = l0 and l2 -- test
		end -- forloop
	else -- jmp
		for k,v in ipairs(l5) do
			l4 = l5 or l6 -- testset
		end -- tforprep, tforcall, tforloop
	end
	do
		local l21, l22 = ... -- vararg
		local function f2() -- closure
			return l21, l22
		end
		f2(k,v) -- call
	end -- close
	local l23 = (l8 // l4) & (~l3) | (l5 << l2) ~ (l6 >> l1) -- idiv band bor bxor shl shr bnot
	local l24 = 22136 -- loadi
	local l25 = 370.5 -- loadk / loadf
	local l26 = "".."abc" -- shrstr
	local l27 = [[
	12345678901234567890123456789012345678901234567890
	12345678901234567890123456789012345678901234567890
	12345678901234567890123456789012345678901234567890
	]]-- lngstr
	local l28 = (l1 == 2) -- lfalseskip
	return f1() -- return, tailcall
end
