/*
 * parser --  2006 - 12 - 12
 *
 *   function ( arg, arg( x,y), ... )
 *     where "\" escapes any single character, 
 *    and an "arg" may have white-space, non-leading, trailing. 
 *    
 * ----------------------------------------------------	-- 
 *    The first application is a browser:
 *       - memory, dictionary, ...
 * ----------------------------------------------------	-- 
 *
 */
#include "cummings.h"
# define is_eec_delim(ch)	\
  ((ch) == '(' ||		\
   (ch) == ',' ||		\
   (ch) == ')')
#define	HERES_YOUR_TOKEN	c_token
#define GETC geteech()		/* define GETC ((char)getc( *rsp)) */

char *TokenList[1000];		/* LOCAL ?? */
int  iTl = 0;
static char waitingChar  = ' ';	/* always One character waiting	*/
LOCAL char *alltokens[5];	/* Token, LeftParen, Comma, RightParen, NULL */
				/* GETC (rsp) is coupled to BufferWithEndPointer
				 */
BufferWithEndPointer( char,HERES_YOUR_TOKEN, 4096, tp, et);
BufferWithEndPointer( FILE *, readstack, 20, rsp, erp);

LOCAL void tok_init()
{
	alltokens[EEC_TID_TOKEN]	= HERES_YOUR_TOKEN;
	alltokens[EEC_TID_LEFT_PAREN]	= strsave("(");  
	alltokens[EEC_TID_COMMA]	= strsave(",");
	alltokens[EEC_TID_RIGHT_PAREN]	= strsave(")"); 
} 
/*
 *   save the incoming tokens 
 *    = cheap, but effective debugging
 */
LOCAL char geteech()
{
  char r =(char)getc(*rsp); 
  fprintf( stderr, "%c", r);
  return (r);
}
LOCAL void set_TokenList( char *t)
{
	TokenList[iTl++] = strsave( t);
}
LOCAL int rWc( char lc)
{
	waitingChar = GETC; 		
	return(	(lc == '(')? 	EEC_TID_LEFT_PAREN: 
		(lc == ')')? 	EEC_TID_RIGHT_PAREN:
		(lc == ',')? 	EEC_TID_COMMA:
				EEC_TID_NO_SUCH_TOKEN);
	
}
/* need an inbuf stack to handle the potentially nested include,
 * such that when a file is parsed, the stack is poped to the current
 * input stream.  
 * 
 * one could also stipulate there are no unbalenced parens in any file,
 * the state is returned to neutral. no uncompleted definitions started
 * in the current file?
 */
LOCAL void file_parser( FILE *fp)
{
  for ( *(++rsp) = fp; rsp < erp && rsp >=readstack; rsp--)
    {
      eec_parser( ); 
    }
  if( rsp >= erp)
    {
      fprintf( stderr, "INPUT Stack OVERFLOW\n");
      exit(  EEC_EXIT_INPUT_OVFL);
    }
}
LOCAL FILE *eec_fread( char *name)
{
  FILE *fp;
  fp = fopen( name, "r");
  if( ! fp ) 
    {
        eec_error("Failed to Open: %s", name, 1); 
    }
    return fp;
}
LOCAL void local_init()
{
  name_function("file_parser", file_parser);
  name_function("eec_fread",   (pfv)eec_fread);
}
LOCAL int is_parserobj_init;

USER char *s_token;		/* state sentinals */
USER char *l_paren;
USER char *r_paren;
USER char *comma;

USER void parserobj_init()
{
  if( is_parserobj_init++) return; 
  
  tok_init();
  compiler_init();
  local_init();
}
USER char *getTheToken()
{
	return HERES_YOUR_TOKEN;
}
USER void ptl()
{
	int i; 
	
	fprintf(stderr, "\n------------------------------\nptl -- Print the Token List --\n");
	for ( i = 0; i < iTl ; i++)
	{
		fprintf(stderr, "%3d %s\n", i, TokenList[i]);
	}
}
USER int getok()
{	
	char *p;			/* fixed Token buffer		*/
	char *q;			/* gives default trim( ... ) !	*/
	int r;
	while ( waitingChar !=EOF && isspace(waitingChar))
	{
		waitingChar = GETC;
	}
	if ( is_eec_delim(waitingChar))
	{
		return rWc( waitingChar);
	}
	if (waitingChar == EOF)
	{
		return EEC_TID_NO_SUCH_TOKEN;
	}
	p = HERES_YOUR_TOKEN;		/* fixed Token buffer		*/
	q = p;				/* gives default trim( ... ) !	*/
	*p = waitingChar;		/* always One character waiting	*/
	while(p < et)
	{
		int t = is_eec_delim(waitingChar);
		if ( t ) break;
		if( ! isspace(waitingChar)) q = p;	/* move end marker 	      */
		if( waitingChar == '\\') 
		{
			waitingChar = GETC;	/* accept escaped character   */
		}
		*p++ = waitingChar;	 
		waitingChar = GETC;	/* store+fetch next character */
	}
	*(++q) = (char)NULL;		/* last non-terminal non-space */
	set_TokenList( HERES_YOUR_TOKEN);
	r = EEC_TID_TOKEN;
	return r;
}
USER void parser()
{
	*rsp = stdin;		/* remove if command line fopen succeeds */
	file_parser( eec_fread( readFile()));
}
