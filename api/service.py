class GS1EvaluatorDFA:
    def __init__(self):
        self.state = 'q0'
        self.final_states = {'q61'}  

    def is_valid_letter(self, char):
        return char.isalpha()

    def is_valid_number(self, char):
        return char.isdigit()

    def transition(self, current_state, char):
        print(f"Transición: Estado actual: {current_state}, Carácter: {char}")

        if current_state == 'q0':
            if char == '(':
                return 'q1'
        elif current_state == 'q1':
            if char == '0':
                return 'q2'
        elif current_state == 'q2':
            if char == '1':
                return 'q3'
        elif current_state == 'q3':
            if char == ')':
                return 'q4'
        elif current_state in ['q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10', 
                               'q11', 'q12', 'q13', 'q14', 'q15', 'q16', 'q17']:
            if self.is_valid_number(char):
                return f'q{int(current_state[1:]) + 1}'

        ##(17)
        elif current_state == 'q18':
            if char == '(':
                return 'q19'
        elif current_state == 'q19':
            if char == '1':
                return 'q20'
        elif current_state == 'q20':
            if char == '7':
                return 'q21' 
        elif current_state == 'q21':
             if char == ')':
                return 'q22' 
             

        ##validacion7-7
        elif current_state == 'q22':  
            if char in '02468':  #YY
                return 'q24'
            elif char in '13579':  ##YY
                return 'q25'
        elif current_state == 'q24':  
            if char in '048':  
                return 'q26'
            elif char in '1235679':  
                return 'q27'
        elif current_state == 'q25':  
            if char in '026':  
                return 'q30'
            elif char in '13579': 
                return 'q31'

        # MM
        elif current_state == 'q26': 
            if char == '0':
                return 'q28'
            elif char == '1':
                return 'q29'
        elif current_state == 'q27': 
            if char == '0':
                return 'q32'
            elif char == '1':
                return 'q33'
        
        # MM
        elif current_state in ['q28', 'q29', 'q30', 'q31', 'q32', 'q33']:
            if char in '123456789':
                return 'q35' 
            elif char == '0':
                return 'q34'  # E,D
        
        
        elif current_state == 'q35':  
            if char in '123456789':  
                return 'q40'
            elif char == '0':  
                 return 'q41'
        
        elif current_state == 'q36': 
            if char in '0-9':
                return 'q42'

        elif current_state == 'q37':  ## feb bi
            if char in '0-9':
                return 'q43'
        elif current_state in ['q40', 'q41', 'q42', 'q43']:
            return 'q45'  
        
        elif current_state == 'q45':
            if char == '(':
                return 'q46'
        elif current_state == 'q46':
            if char == '1':
                return 'q47'
        elif current_state == 'q47':
            if char == '0':
                return 'q48'
        elif current_state == 'q48':
            if char == ')':
                return 'q49'
        elif current_state in ['q49', 'q50', 'q51']: 
            if self.is_valid_letter(char):
                return f'q{int(current_state[1:]) + 1}'
        elif current_state == 'q52':  
            if self.is_valid_number(char):
                return 'q53'
        elif current_state == 'q53':
            if self.is_valid_number(char):
                return 'q54'
        elif current_state == 'q54':
            if self.is_valid_number(char):
                return 'q55'

        # (30)
        elif current_state == 'q55':
            if char == '(':
                return 'q56'
        elif current_state == 'q56':
            if char == '3':
                return 'q57'
        elif current_state == 'q57':
            if char == '0':
                return 'q58'
        elif current_state == 'q58':
            if char == ')':
                return 'q59'
            # 
        elif current_state == 'q59':
            if self.is_valid_number(char):  
                return 'q60'  
            elif char == 'e':  
                return 'q62' 

        elif current_state == 'q60':
            if self.is_valid_number(char):
                return 'q61'  
            elif char == 'e':  
                return 'q62'  

        elif current_state == 'q61':
            if self.is_valid_number(char): 
                return 'q62' 
            elif char == 'e':  
                return 'q62'  
        elif current_state == 'q62':
            return 'valid' 


        print(f"Carácter no esperado: {char} en el estado {current_state}, transición inválida.")
        return 'invalido'

    def evaluate_gs1(self, code):
        self.state = 'q0'
        print(f"Evaluando código: {code}")
        
        for char in code:
            self.state = self.transition(self.state, char)
            
            # Si hay una transición inválida, se detiene la evaluación
            if self.state == 'invalido':
                print("Código GS1-128 inválido")
                return False
            
            # Si alcanza un estado final, se detiene la evaluación
            if self.state in self.final_states:
                print(f"Estado final alcanzado: {self.state}")
                print("Código GS1-128 válido")
                return True
        
        # Verificación final después de procesar todos los caracteres
        if self.state in self.final_states:
            print("Código GS1-128 válido")
            return True
        else:
            print("Código GS1-128 inválido")
            return False




class GS1EvaluatorService:
    @staticmethod
    def evaluate_code(code: str) -> str:
        dfa = GS1EvaluatorDFA()
        cleaned_code = code.strip()
        if dfa.evaluate_gs1(cleaned_code):
            return "Código GS1-128 válido"
        else:
            return "Código GS1-128 inválido"

    @staticmethod
    def evaluate_file(file_content: str):
        results = []
        codes = file_content.strip().splitlines()
        
        for code in codes:
            result = GS1EvaluatorService.evaluate_code(code)
            results.append({"code": code, "result": result})
        
        return results


# Ejemplo de uso
code_to_evaluate = "(01)12345678901234(17)240229(10)LOT156(30)56"
result = GS1EvaluatorService.evaluate_code(code_to_evaluate)
print(result)
