<!-- Guardrails
validate user input and agent output
5 classes and 2 decoraters
run parallel with agent
guardrail is like func return class GuardrailFunctionOutput
in GuardrailFunctionOutput 2 keys 
1. output info  -> save result in output
2. trip-wire-triggered  -> decide to generate error -->

<!--
 Guardrail basically is a func 
GuardrailFunctionOutput ek class ha
jis men 2 keys hote hen 
    1.Output info
    wo result jo save krna chahte hen
    2.Tripwire_triggered 
    ya decide krti ha error generate krna ha ya nahi
    tripwire = true  -> error
    tripwire = flase  -> not error
tripwire_trigerred true hoga tu class ha 
input_guardrail_tripwire_triggered,output_guardrail_tripwire_triggered
iss men hamara guardrail result ata ha ya agentExeption se inherit ho rahi ha

InputGuardrailResult ek class
jis 2 keys hen
1.guardrail
func rakha jata hai
2.output
jo func ka output hoga wo 
-----------------------------
guardrail 2 jaga pass kr 
runcofig runner men

input guardrail first turn men run hoga
-->
