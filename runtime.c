/* runtime -- 2006-12-22
 *
 * build the runtime machine:
 * 
 * runs off a TAPE, which has one of three types of information, a
 * built-in instruction, such as a JUMP, or a conditional Jump, these
 * accompanied the second type ofinformation: an Address, and finally a
 * default type, an address of a Word.  This word contains a name
 * (pointer to character string), a value, which may be set or fetched,
 * and finally, a function pointer, which is direct code to execute.
 * 
 *  
 * code:
 *    push next instruction pointer to runtime stack
 *    set lptr to start of code;   
 * 
 * retn:
 *    move the a(i) to the call/return stack by the frame ptr
 *    jump to popped runtime stack
 *   
 */

#include <stdio.h>
#include "cummings.h"

#define	IPTR	((int)*ip++)
#define	DICT_IP	((Word *)(*ip))
#define	PRE_DECR(x,y)	(--(x))
#define	POST_INCR(x,y)	((x)++)

#define	VoidPop(type,x)	((type)*(--(x)))
#define	VoidPush(pc,val)	(*(pc)++) = ((long)(val))
#define	VoidSet(addr,val)	(*(addr)) = ((long)(val))

#define	sPpush(x)		VoidPush(sptr, x)
#define	fRpop(x)		VoidPop( ifrm, x)
#define	fRpush(x)		VoidPush(ifrm, x)

#define	TAKE_DATA(cval, addr, val)		\
  case cval:					\
  for( i=0, n = data[i]; n>0; n--) {		\
    i++;					\
    *(addr) = data[i];				\
    POST_INCR(addr,val);	}			\
  return;					\
  break

#define	GIVE_DATA(cval, addr, val)		\
  case cval:					\
  PRE_DECR(addr,val);				\
  data[0] = *(addr);				\
  return;					\
  break

/*
 * Post Increment allows FRAME pointer to be set to the empty, and expecting stack pointer.
 */

/*
 * three objects, seven values of interest:
 *	FRAME & current Frame pointer
 *	STACK & current stack pointer
 *	TAPE,	compile pointer, and instruction pointer
 */

#define	DEBUG	debug( frame, ifrm, stack, sptr, tape, (long *)cptr, (long *)ip)

LOCAL void memptr( char *msg, long *iptr, long *eptr,int type)
{	
  fprintf( stderr, "%s\n", msg);
  if (iptr >= eptr)
    {
      return;
    }
  for (
       iptr = ((iptr < eptr - 16)? eptr - 16: iptr);
       iptr < eptr; iptr ++
       )
    {
      fprintf(stderr, "               %8x: %x\n", iptr, *iptr);
      switch ( type )
	{
	case 2:
	  d_prnode((Word *)*iptr);
	  break;
	}
    }
}	 


LOCAL void debug(
		  long *frm, long *f_ptr, 
		  long *stk, long *s_ptr,
		  long *tp,  long *cmp, long *insp
		  )
{
  ptl();
  memptr( "FRAME STACK", frm, f_ptr,1);
  memptr( "Data  STACK", stk, s_ptr, 2);
  memptr( "The Tape:",   (long *)tp, cmp,2);
  
  return; 
}
/*
 * ------------------------------------------------------------------- COMMANDS	--
 */
enum command_name 
{
  NO_COMMAND, 
  RT_INIT,
  PUSH,
  COPY,
  KEEP,
  POP,
  FRAME,
  CLEAR,
  TOTAPE,
  TURING,
  EXTOKN,
  STAK_TAPE,
  WHERE,
  BEGIN,	
  STK_FRM
};
LOCAL long *doWord(void *wq, long *tops)
{
  return tops;
}
/*
 * -------------------------------------------------------------------- RUNTIME	--
 */
void runtime( long *data, int message)
{
  static long *ip; 		/* the current instruction pointer	*/
  static long *cptr;		/* where to copy instructons		*/
  static long *eotp;		/* end of Tape				*/
  static long tape[4096];		/* the start of the tape		*/
  static long tape_size;
  
  static long stack[4096];	/* the data stack			*/
  static long *sptr;		/* current storage location		*/
  static long *tops;		/* top of Stack 			*/
  
  static long frame[256];	/* the frame pointer			*/
  static long *ifrm;		/* its current frame pointer		*/
  static long *efrm;		/* end of Frame 			*/
/*
  static Word *tocall; 
  static void *wq;		/* good place for a UNION		*/
  static long i;
  static long n;
  
  /*
   * ------------------------------------------------------------------------ COMPILING	--
   */
  switch ( message )
    {
      
    case RT_INIT:
      tape_size = 4096;
      /* 
       * save this for later
       * tape = (TAPE)malloc( (long)tape_size); 
       */
      ip = cptr = tape; eotp = &tape[tape_size];
      sptr = stack;     tops = &stack[4096];
      ifrm = frame;     efrm = &frame[256];
      DEBUG;
      return;
      break;
      /*      TAKE_DATA( PUSH, sptr, tops); */
    case KEEP:
      sptr++;
      DEBUG;
      return;
      break;      
    case COPY:
      for( i=0, n = data[i]; n>0; n--) {
	i++;
	*sptr = data[i];
      }
      DEBUG;
      return;
      break;      
    case PUSH:
      for( i=0, n = data[i]; n>0; n--) {
	i++;
	assertion( 301, sptr < tops, "runtime Stack OVERFLOW");
	*sptr = data[i];
	sptr++;
      }
      DEBUG;
      return;
      break;      
      /*      GIVE_DATA( POP,  sptr, stack); */
    case POP:
      /*  PRE_DECR(sptr,stack); */
      --sptr;
      data[0] = *(sptr);
      DEBUG;
      return;
      break;
      
      /*      TAKE_DATA( FRAME, ifrm, efrm); */
    case FRAME:
      for( i=0, n = data[i]; n>0; n--) {
	i++;
	assertion( 303, ifrm < efrm, "Stack Frame OVERFLOW");
	*ifrm = data[i];
	ifrm++;
      }
      DEBUG;
      return;
      break;
      
      /*      GIVE_DATA( CLEAR, ifrm, frame); */
    case CLEAR:
      /*  PRE_DECR(ifrm, frame); */
      --ifrm;
      data[0] = *(ifrm);
      DEBUG;
      return;
      break;
      
    case TOTAPE:
      for( i=0, n = data[i]; n>0; n--) {
	i++;
	assertion( 302, eotp > cptr , "TAPE is FULL ");
	*cptr = data[i];
	cptr++;
      }
      DEBUG;
      return;
      break;

    case STK_FRM:
	*ifrm++ = (long)sptr;
      DEBUG;
      return;
      break;
      
    case TURING:	
      /* EDIT_MARK */
      data[1] = cptr - tape;
      data[2] = ip   - tape;
      DEBUG;
      return; 
      break;
      
    case EXTOKN:
      /* PRE_DECR(sptr,stack); */
      --sptr;
      *cptr = *sptr; 
      cptr++;
      /*      POST_INCR(cptr,eotp); */
      DEBUG;
      break;

    case STAK_TAPE:
      while ( sptr > stack )
	{
	  --sptr;
	  *cptr = *sptr;
	  cptr++;
	}
      DEBUG;
      break;
    case WHERE:
      data[0] = (long)cptr;
      DEBUG;
      return;
      break;
    case BEGIN:
      DEBUG;
      break;			/* execution			*/	
    default:
      DEBUG;
      eec_error("ILLEGAL MESSAGE: %d\n", "",  (int)message);
      break;
    }
  /*
   * ---------------------------------------------- EEC Virtual Machine	--
   */
  fRpush( sptr); 
  while ( 1 )
    {
      DEBUG; 
      switch ((int)*ip++)
	{
	case (long)0:
	  DEBUG;
	  return;
	  break;
	case EEC_RT_END_OF_LIST:
	  break;
	case EEC_RT_IFNO:
	  break;
	case EEC_RT_JUMP:
	  break;
	  /*
	   * case EEC_RT_PUSH: 
	   * sPpush(ifrm);		/* ?? calling argument
	   * break; 
	   * 
	   * case EEC_RT_CODE:
	   * fRpush( ip+1); 
	   * fRpush( sptr);
	   * tocall = DICT_IP;
	   * ip = (TAPE )get_thred( tocall); /* TO FIX
	   * if( ! ip)
	   * {
	   * fprintf( stderr, "BAD Code RETURNing from Word:");
	   * /*     d_prword( tocall);		
	   * exit( EEC_EXIT_RT_BAD_WORD);
	   * }
	   * 
	   * break;
	   * 
	   * case EEC_RT_CALL:
	   * /* tocall = DICT_IP;
	   * run_funct( tocall, ip);	/* built-in function 
	   * 
	   * break; 
	   * case EEC_RT_RETN:		
	   * /* Ugly, but effective
	   * *ifrm = ifrm[IPTR]; 	/* return value
	   * ifrm--;			/* safely pop
	   * ip = fRpop( long *);
	   * if( ! IPTR)
	   * {
	   * fprintf( stderr, "BAD Code.  HOLE in the TAPE:");
	   * exit( EEC_EXIT_RT_TAPE_HOLE);
	   * }
	   * 
	   * break;
	   * case EEC_RT_NAME:
	   * break; 
	   * case EEC_RT_VALU:
	   * ifrm[0] = *ifrm; ifrm--;
	   * break; 
	   */
	default:
	  --ip;
	  tops = doWord((void *)ip, tops);
	  break;
	}
    }
}

/*
 * ------------------------------------------- Simple Intereactions: One Token to, from	--
 */
static long rt_val[3];

USER void rt_run()		
{
  runtime( rt_val, BEGIN); 
}
USER void rt_stape()		
{
  runtime( rt_val, STAK_TAPE); 
}
USER void rt_keep()
{
  runtime( rt_val, KEEP); 
}
USER void rt_copy(long val)	
{
  rt_val[0]=1L;
  rt_val[1] = (long)val;
  runtime( rt_val, COPY); 
}
USER void rt_push(long val)	
{
  rt_val[0]=1L;
  rt_val[1] = (long)val;
  runtime( rt_val, PUSH); 
}
USER long rt_pop()		
{
  runtime( rt_val, POP);
  return rt_val[0]; 
}
USER void rt_stack_frame()	
{
  runtime( rt_val, STK_FRM); 
}
USER void rt_frame(long val)	
{
  rt_val[0]=1L;
  rt_val[1] = (long)val;
  runtime( rt_val, FRAME); 
}

USER long rt_clear()		
{
  runtime( rt_val, CLEAR);
  return rt_val[0]; 
}
USER void rt_tape(long val)	
{
  rt_val[0]=1L;
  rt_val[1] = (long)val;
  runtime( rt_val, TOTAPE); 
}

USER TAPE rt_qtape()		
{
  runtime( rt_val, WHERE);
  return (TAPE )rt_val[0];
  
} 
USER TAPE rt_turing()		
{
  runtime( rt_val, TURING);
  return (TAPE )rt_val;
  
}
USER TAPE save_cell()		
{
  long rt = rt_qtape();
  rt_tape((long)0);
  return rt;
  
}      
USER void stuff_ip_at(long *px)	
{
  *px = (long)rt_qtape();
}

static is_runtime_init = 0;
USER void runtime_init()
{	
  if (is_runtime_init++) return;

  runtime( rt_val, RT_INIT);
}
/*
 * -------------------------------------------------------------------------- TEST CASE	--
 */
#ifdef TESTING
int main( int argc, char *argv[])
{
  long data[4];
  
  runtime_init();
  rt_push( (long)main);
  /* ... */
  
}
#endif
