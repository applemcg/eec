/*
 * cummings --  2006 - 12 - 12
 *
 *   function ( arg, arg( x,y), ... )
 *     where "\" escapes any single character, 
 *    and an "arg" may have white-space, non-leading, trailing. 
 *    
 * ----------------------------------------------------	-- 
 *    The first application is a browser:
 *         - memory, dictionary, ...
 */
#ifndef _CUMMINGS_H
#define _CUMMINGS_H
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
/*
 * All the structure typedefs are here for all to see
 * and not structure members are directly visible to users
 */
typedef struct word	Word;
/* typedef struct Compiler	Compiler; */
typedef struct Type	Type;
typedef struct dntry Dntry;
typedef char *pchar;
typedef int (* pfi) ();		/* Pointer to Function returning int */
typedef long (* pfl) ();	/* Pointer to Function returning long */
typedef void (* pfv) ();	/* Pointer to Function returning void */
typedef char (* pfc) ();	/* Pointer to Function returning Char  */
typedef pchar (* pfcp) ();	/* Pointer to Function returning Char*  */
typedef int PFP;
typedef long  TAPE;		/* the Turing Tape */
#define New(name) 	((struct name *)malloc(sizeof(struct name)))
#define BufferWithEndPointer(type, buf, size, ptr, ept) \
type buf[size];		    			\
type *ptr = buf;					\
type *ept = buf+size
enum parser_state 
{
	/* states of the parser, building tokens */
	S_START,			/* haven't seen anything yet */
	S_TOKEN,			/* it was a token */
	S_LPAREN,			/* a left parenthesis, "(" */
	S_COMMA,			/* a comma */
	S_RPAREN,			/* it was a right parenthesis ")" */
	S_END				/* at EOF on stdin */
}
;
enum token_compiler_state 
{
	/* when compiling */
	T_NO_STATE,			/* none, yet */
	T_COMPILING,			/*  ... */
	T_END_OF_LIST			/* spare ... */
}
; 
#define NAME_TYPE 1
#define FUNC_TYPE 2
enum eec_exit_code 
{
	EEC_EXIT_DONT_USE,
	EEC_EXIT_RT_BUILTIN,
	EEC_EXIT_INPUT_OVFL,
	EEC_EXIT_RT_BAD_WORD,
	EEC_EXIT_RT_TAPE_HOLE,
	EEC_EXIT_CP_TAPE_OVRW,
	EEC_EXIT_CP_WHIL_COMA,
	EEC_EXIT_CP_IF_COMA,
	EEC_EXIT_NO_OI,
	EEC_EXIT_END_OF_LIST
}
; 
enum eec_runtime_code 
{
	/* internal, run-time code	*/	
	EEC_RT_DONT_USE,     		/* in case it's zero		*/
	EEC_RT_PUSH,			/* push an argument		*/
	EEC_RT_CODE,			/* it's more internal code	*/
	EEC_RT_CALL,			/* it's a built-in function	*/
	EEC_RT_IFNO,			/* If the stack is false, JUMP	*/
	EEC_RT_JUMP,			/* Absolute Jump 		*/
	EEC_RT_VARL,			/* it's a variable		*/
	EEC_RT_SET,			/* it's a SET			*/
	EEC_RT_CONSTANT,		/* it's a CONSTANT		*/
	EEC_RT_COMMENT,		/* it's a CONSTANT		*/
	EEC_RT_WHILE,			/* it's a WHILE loop		*/
	EEC_RT_IF,			/* it's an IF stmt		*/
	EEC_RT_RETN,			/* return from run-time code	*/
	EEC_RT_VALU,			/* return the value of the word */
	EEC_RT_NAME,			/* return the name of the word	*/
	EEC_RT_ADD,
	EEC_RT_SUBTRACT,
	EEC_RT_MULTIPLY,
	EEC_RT_DIVIDE,
	EEC_RT_MOD,
	EEC_RT_AND,
	EEC_RT_OR,
	EEC_RT_EXCLUSIVE_OR,
	EEC_RT_LESS,
	EEC_RT_GREATER,
	EEC_RT_EQUAL,
	EEC_RT_LESS_OR_EQUAL,
	EEC_RT_GREATER_OR_EQUAL,
	EEC_RT_INCREMENT,
	EEC_RT_DECREMENT,
	EEC_RT_NOT,
	EEC_RT_0,
	EEC_RT_1,
	EEC_RT_2,
	EEC_RT_END_OF_LIST		/* so inserts are with ,'s	*/
}
;
/* from turning.c		*/
#define	EEC_TID_NO_SUCH_TOKEN  0
#define	EEC_TID_TOKEN	       1
#define	EEC_TID_LEFT_PAREN     2
#define	EEC_TID_COMMA	       3
#define	EEC_TID_RIGHT_PAREN    4
#define	EEC_TID_END	       5
#define	EEC_TID_START	       6
#define	EEC_TID_END_OF_LIST    7
#define IMMEDIATE_ATTRIB 1  	/* powers of two	*/
#define EXECUTE_COMPILING 2	/* as Flags		*/
typedef struct STRING
{
	struct STRING *s_next;
	int	         s_length;
	char          *s_text;
}
STRING ; 
#define wsalloc malloc
#include "externals.h"
#define USER			
#define LOCAL static		/* hides the interface to funtions, variables */
#endif
