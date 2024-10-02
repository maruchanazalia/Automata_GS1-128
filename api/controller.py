from api.service import GS1EvaluatorDFA

async def validate_gs1_code(input_string):
    dfa = GS1EvaluatorDFA()
    validation_result = dfa.process(input_string) 
    
    if validation_result["status"] == "success":
        return {"status": "success", "message": "Código GS1-128 válido"}
    else:
        return {
            "status": "error",
            "message": "Código GS1-128 inválido",
            "details": validation_result["details"] 
        }
