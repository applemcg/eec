/* compiler.c -- 2010-05-22
 *
 *   run-time aspects,  
 *     input is now all Compiled to the TAPE, from where
 *     it is then executed.
 */

#include "cummings.h"

#define write_code(cx)  (rt_tape( (TAPE) (cx)))
#define STUFF_IP_AT(wd) (stuff_ip_at((long *)wd))
#define COMMA_COUNT(p)  ((p)->c_count)

#define EMIT(wa, wb)			\
  write_code( (TAPE)wa);		\
  write_code( (TAPE)wb)

LOCAL void failedAssert( int ex, char *errmsg)
{
  fprintf( stderr, errmsg);
  exit(ex);
}
USER void assertion(int ex, int cond, char *errmsg)
{
  if( !cond)	
    {
      failedAssert(ex, errmsg);
    }
}
struct compiler
{
  char *name;
  struct dntry *c_word;	
  long *addr[3];	/* addresses A, B, C;		*/
  long *c_pdata;	/* my base on the data stack	*/
  int c_count;		/* comma Count			*/
  Type *c_type;		/* what type is this one	*/
  
};

LOCAL struct compiler *cStack[128];		/* less ugly, N-level parens	*/
LOCAL struct compiler **pcStack;		/* where is the compiler now	*/  

LOCAL void toPc(struct compiler *pc)
{
  pcStack++;
  *pcStack = pc;
}
LOCAL void offPc()
{
  --pcStack;
}
LOCAL struct compiler *getPc()
{
  assertion( 105, (*pcStack !=(struct compiler *)NULL), "Compile Stack is EMPTY");
  return *pcStack;
}
LOCAL struct compiler *initPc() 
{
  pcStack = cStack;
  return  *pcStack;
}
LOCAL struct compiler *new_Compiler()
{
  struct compiler *q	= New( compiler);
  q->c_count	= -1;			/* await default_Lparen */
  q->c_pdata	= pData();
  return q;
}
LOCAL void next_compiler( Type *tp)
{	
  /* compare to init_compiler, generalize?? */
  struct compiler *pc = new_Compiler();
  pc->c_type = tp; 
  toPc( pc);
}
LOCAL void wrap_compiler()
{
  rt_stape();		/* to the tape			*/
  rt_pop();		/* from the stack		*/
  rt_run();		/* while interpreting		*/
}

/* --------------------------------------------------------------- Type	--
 */
struct Type 
{
  int t_nargs;		/* number of fixed args 	*/
  int t_vargs;		/* any variable args		*/
  pfv t_func;		/* the compiler			*/
};
/*
 * --------------------------------------------------------- data_stack	--
 */

static long data_stack[1024];
static long *pdata;
static long *edata;

USER void pushData( long d) 
{ 
  assertion( 101, (pdata < edata), "pushData: stack Overflow");
  *pdata++ =  d;
}
USER long *pData()
{
  return pdata;
}
USER long popData ()
{
  assertion( 102, (pdata >= data_stack), "pushData: stack UNDERFLOW");
  return *(--pdata);
}
LOCAL void initData()
{
  pdata = data_stack;
  edata = &data_stack[1024];
  assertion( 103, (pdata < edata), "pushData: INIT stack Overflow");
  assertion( 104, (pdata >= data_stack), "pushData: INIT stack UNDERFLOW");
}
LOCAL void init_compiler( Type *pOI)
{
  struct compiler *pc;
  initData();
  cStack[0] = new_Compiler();
  pc = initPc();
  pc->c_type = pOI; 
}
LOCAL void handleToken(struct compiler *pc, char *token)
{
  Type *tp;
  struct dntry *dw = d_search( token); 
  if( dw == (struct dntry *)NULL)
    {
      dw = thisWord( token, (long)NULL, EEC_RT_VARL);
    }
  if( tp = isTyped(dw) )
    {
      next_compiler(tp);
    }
  rt_copy((TAPE)dw);	/* see LEFT_PAREN */
}
/* ---------------------------------------------------- Generic	--
 */
LOCAL void c_generic(struct compiler *pc, int token, char *fname)
{
  Type *t;
  int cc;
  switch ( token )
    {
    case EEC_TID_TOKEN:
      handleToken(pc, getTheToken());
      break;
    case EEC_TID_LEFT_PAREN:
      pc->c_count = 0; 
      rt_keep();	/* copy + keep = push */
      break;
    case EEC_TID_COMMA:
      cc = pc->c_count++;
      t = pc->c_type;
      if( (!t->t_vargs) && cc >= t->t_nargs)
	{
	  eec_error("Too Many Args in %s", fname, 201);
	}
      break;
    case EEC_TID_RIGHT_PAREN:
      offPc();
      wrap_compiler();
      break;
    case EEC_TID_NO_SUCH_TOKEN:
      eec_error("No such token in $s", fname, 202);
      break;
    case EEC_TID_END:
      exit(0);
      break;
    case EEC_TID_START:
      /* NO-OP */
      break;
    case EEC_TID_END_OF_LIST:
      /* Fall thru to Default */
    default:
      eec_error("No such Token STATE in %s", fname, 101);
      break;
    }
}
/*
 * -------------------------------------------------- Outer Interpreter	--
 */
LOCAL void c_interpreter(struct compiler *pc, int token)
{
  char *fname = "c_interpreter";
  switch ( token )
    { 
    default:
      c_generic(pc, token, fname);
      break;
    }
}
/* 
 * --------------------------------------------------- Compiler	--
 */
LOCAL void c_compiler(struct compiler *pc, int token)
{
  char * fname = "c_compiler";
  switch ( token )
    { 
    case EEC_TID_TOKEN:
      break;
    default:
      c_generic( pc, token, fname);
      break;
    }
}
/* 
 * --------------------------------------------------- Comment	--
 */
LOCAL void c_comment(struct compiler *pc, int token)
{
  char * fname = "c_comment";
  switch ( token )
    { 
    case EEC_TID_LEFT_PAREN:
      pc->c_count++;
      break; 
    case EEC_TID_RIGHT_PAREN:
      pc->c_count--;
      if (pc->c_count < 1) 
	{
	  c_generic( pc, token, fname);
	}
      break; 
    default:
      c_generic( pc, token, fname);
      break;
    }
}
/* 
 * -------------------------------------------------------- Set	--
 */
LOCAL void c_stacktwo(struct compiler *pc, int token)
{
  char * fname = "c_stacktwo";
  switch ( token )
    { 
    default:
      c_generic( pc, token, fname);
      break;
    }
}
/* 
 * --------------------------------------------------- Constant	--
 */
LOCAL void c_constant(struct compiler *pc, int token)
{
  char * fname = "c_constant";
  char *tok = getTheToken();
  Dntry *dw; 
  switch ( token )
    { 
    case EEC_TID_TOKEN:
      dw = thisWord(tok, atoi(tok), EEC_RT_CONSTANT);
      break;
    case EEC_TID_RIGHT_PAREN:
      offPc();
      break;
    default:
      c_generic( pc, token, fname);
      break;
    }
}
/* 
 * ------------------------------------------------------ While	--
 */
LOCAL void c_while( struct compiler *pc, int token)
{
  char * fname = "c_while";
  switch ( token )
    {
    case EEC_TID_TOKEN:

      break;
    default: 
      c_generic( pc, token, fname);
      break;
    }
}
/*
 * --------------------------------------------------------- If	--
 */

LOCAL void c_if( struct compiler *pc, int token)
{
  Type *t;
  char * fname = "c_if";
  int cc;

  switch ( token )
    {
    case EEC_TID_COMMA:
      t = pc->c_type;
      cc = pc->c_count++;
      if (cc == 0)
	{
	  write_code( EEC_RT_IFNO);		/* If not TRUE	*/
	  pc->addr[cc] = (long *)save_cell(); 	/* save ELSE	*/
	}
      else if (cc == 1)
	{
	  write_code( EEC_RT_JUMP);		/* If TRUE	*/
	  pc->addr[cc] = (long *)save_cell(); 	/* save END	*/
	  STUFF_IP_AT(pc->addr[0]);		/* FALSE: ...	*/
	}
      else
	{
	  eec_error( "ERROR, Too many Commas in %s\n", "c_if", 211);
	  exit( EEC_EXIT_CP_IF_COMA);
	}
      break;
    case EEC_TID_RIGHT_PAREN:
      STUFF_IP_AT(pc->addr[1]);		/* THEN  ...	*/
      c_generic( pc, token, fname);
      break;
    default: 
      c_generic( pc, token, fname);
      break;
    }
}
USER void eec_error( char *fmt, char *tok, int num)
{
  fprintf( stderr, fmt, tok, num);
  exit( num); 
}
/* ------------------------------------------ OUTER INTERPRETER	--
 *
 * this is THE COMPILER
 *    Compiler  the code 'myTid': token, (, ",", ),  UNDEFINED
 *   appropriate to the particular object: PC, 
 *   with the actual Token:   "alltokens[EEC_TID_TOKEN]"
 *   it probably needs the datastack context as well.
 */
LOCAL void otdb( pfv fn, struct compiler *pc,  int token)
{
}
LOCAL int one_token() 
{
  struct compiler *xy	 =  getPc();	
  Type *ct	= xy->c_type;
  pfv fn	= ct->t_func;		/* the parser for this layer	*/
  int token	= getok();		/* the next token		*/
  switch (token)
    {
    default:
      otdb( fn, xy, token);
      (*fn) ( xy, token);	/* Parser( Compiler, state)	*/
      break;
    }
  return 1; 
}
USER void eec_parser( )
{
  while( one_token( ))
    {
      ;
    }
}
/* --------------------------------------------- Initialization	--
 *
 */

LOCAL Type builtinType[ ] =
  {
    0,	0,	c_interpreter,		/* 0: outer interpreter	*/
    0,	1,	c_generic,		/* 1:   ...		*/
    2,	0,	c_while,		/* 2:   while( p, c )	*/
    3,	0,	c_if,			/* 3:   if( q, t, f )	*/
    2,  0,      c_stacktwo, 		/* 4:    XXX( a, b )	*/
    1,  0,      c_constant, 		/* 5:   constant( 3 )	*/
    1,  0,      c_comment, 		/* 6:   comment(.(.).)	*/
  };

LOCAL void set_bi( char *name, int typeA, long codeValue)
{
  Dntry *j;
  j = thisWord( name, (long)&builtinType[typeA], codeValue);
}
/* EDIT MARK
 *  we have to distinguish between words with only compiler effect
 *  and those leaving an effect on the compiler/tape/runtime stack.
 *  "set" does; "constant" does not.
 */
LOCAL void builtin_init()
{
  set_bi( "set",   4, EEC_RT_SET);	/* Stack Two		*/	      
  set_bi( "while", 2, EEC_RT_WHILE);
  set_bi( "if",	   3, EEC_RT_IF);
  set_bi( "constant",  5, EEC_RT_CONSTANT);
  set_bi( "comment",  6, EEC_RT_COMMENT);
  idBiType( builtinType,  builtinType +  sizeof(builtinType));
}

    int nobj;       /* UNUSED */
LOCAL void OI_init()
{
  nobj = sizeof(builtinType)/sizeof(Type);
  
  init_compiler( &builtinType[0]) ;
}

LOCAL int is_compiler_init;

USER void compiler_init()
{
  if( is_compiler_init++) return; 
  
  dict_init();
  builtin_init(); 
  OI_init();		/* Outer Interpreter		*/
}
