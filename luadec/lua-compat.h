// should be included after lua*.h
#ifndef LUADEC_LUA_COMPAT_H
#define LUADEC_LUA_COMPAT_H

#include "lua.h"

#if LUA_VERSION_NUM == 501
	#define luadec_freearray(L, b, n, t) luaM_freearray(L, b, n, t)

	#define UPVAL_TYPE TString*
	#define NUPS(f) (f->nups)
	#define UPVAL_NAME(f, r) (f->upvalues[r])

	#define LUADEC_TFORLOOP OP_TFORLOOP
	#define FUNC_BLOCK_END(f) (f->sizecode - 1)

	// Lua 5.1 #define LUA_COMPAT_VARARG : is_vararg = 0 2 3 7, 2 is main, 3 and 7 has another parament arg
	// Lua 5.1 #undef LUA_COMPAT_VARARG  : is_vararg = 0 2, 2 is main or which use ..., never use arg
	#define NEED_ARG(f) (((f->is_vararg == 3) || (f->is_vararg == 7))?1:0)
#endif
#if LUA_VERSION_NUM == 501 || LUA_VERSION_NUM == 502
	#define LUA_STRLEN(ts) ((ts)->tsv.len)
#endif
#if LUA_VERSION_NUM >= 502
	#define lua_open()	luaL_newstate()
	#define luadec_freearray(L, b, n, t) luaM_freearray(L, b, n)

	#define UPVAL_TYPE Upvaldesc
	#define NUPS(f) (f->sizeupvalues)
	#define UPVAL_NAME(f, r) (f->upvalues[r].name)

	#define FUNC_BLOCK_END(f) (f->sizecode)

	// Lua >= 5.2 : is_vararg = 0 1 , never use parament arg, but main has a global arg
	#define NEED_ARG(f) 0
#endif
#if LUA_VERSION_NUM == 502 || LUA_VERSION_NUM == 503
	#define LUADEC_TFORLOOP OP_TFORCALL
#endif
#if LUA_VERSION_NUM >= 503
	#define rawtsvalue(o) tsvalue(o)

	#ifdef tsslen
		#define LUA_STRLEN(ts) tsslen(ts)
	#else
		#define LUA_STRLEN(ts) ((ts)->len)
	#endif

	#define MAXREGS 250
	#define MAXSTACK MAXREGS
#endif
#if LUA_VERSION_NUM >= 504
	#include "lopnames.h"
	#define luaP_opnames opnames
	#define LUADEC_TFORLOOP OP_TFORLOOP
	#ifndef ISK
		#define ISK(x) 0
	#endif
	#ifndef INDEXK
		#define INDEXK(x) (x)
	#endif
	#ifndef BITRK
		#define BITRK (1 << 7)
	#endif
#endif
#if LUA_VERSION_NUM >= 505
	#define IS_VARARG(f) (isvararg(f))
	#define GETARG_vB_COMPAT(i) GETARG_vB(i)
	#define GETARG_vC_COMPAT(i) GETARG_vC(i)
	#define TFOR_VAR_OFFSET 2
	#define TFOR_INTERNAL_NUM 3
	#ifndef lua_lock
		#define lua_lock(L) ((void) 0)
	#endif
	#ifndef lua_unlock
		#define lua_unlock(L) ((void) 0)
	#endif
#else
	#define IS_VARARG(f) (f->is_vararg)
	#define GETARG_vB_COMPAT(i) GETARG_B(i)
	#define GETARG_vC_COMPAT(i) GETARG_C(i)
	#define TFOR_VAR_OFFSET 3
	#define TFOR_INTERNAL_NUM 4
#endif

#endif // #ifndef LUADEC_LUA_COMPAT_H
