extern Word *new_word ( char *name);
extern Dntry *thisWord( char *name, long val, long code);
extern void idBiType(Type *biOrigin, Type *biEnd);
extern Type *isTyped(Dntry *dw);
extern pfv get_thred( Word *tocall);
extern void d_prnode( Word *p);
extern void name_function( char *name, pfv funct);
extern void word_init();
