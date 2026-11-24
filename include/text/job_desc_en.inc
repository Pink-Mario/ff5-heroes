.list off
.ifndef JOB_DESC_INC
JOB_DESC_INC = 1

.global JobDesc, JobDescPtrs

.scope JobDesc

        Start := bank_start JobDesc

; ##############################################################################
; ###          AUTOMATICALLY GENERATED CODE, DO NOT MODIFY MANUALLY          ###
; ##############################################################################

        ARRAY_LENGTH = 22

        _0 := JobDesc + -1611
        _1 := JobDesc + 24
        _2 := JobDesc + 44
        _3 := JobDesc + 87
        _4 := JobDesc + 88
        _5 := JobDesc + 141
        _6 := JobDesc + 155
        _7 := JobDesc + 172
        _8 := JobDesc + 173
        _9 := JobDesc + 212
        _10 := JobDesc + 213
        _11 := JobDesc + 214
        _12 := JobDesc + 215
        _13 := JobDesc + 216
        _14 := JobDesc + 247
        _15 := JobDesc + 284
        _16 := JobDesc + 285
        _17 := JobDesc + 326
        _18 := JobDesc + 371
        _19 := JobDesc + 372
        _20 := JobDesc + 373
        _21 := JobDesc + 421

; ##############################################################################

.endscope

.endif
.list on
