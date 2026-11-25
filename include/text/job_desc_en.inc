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

        _0 := JobDesc + 0
        _1 := JobDesc + 23
        _2 := JobDesc + 42
        _3 := JobDesc + 85
        _4 := JobDesc + 86
        _5 := JobDesc + 139
        _6 := JobDesc + 152
        _7 := JobDesc + 168
        _8 := JobDesc + 169
        _9 := JobDesc + 208
        _10 := JobDesc + 209
        _11 := JobDesc + 210
        _12 := JobDesc + 211
        _13 := JobDesc + 212
        _14 := JobDesc + 243
        _15 := JobDesc + 279
        _16 := JobDesc + 280
        _17 := JobDesc + 320
        _18 := JobDesc + 365
        _19 := JobDesc + 366
        _20 := JobDesc + 367
        _21 := JobDesc + 415

; ##############################################################################

.endscope

.endif
.list on
