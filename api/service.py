class GS1EvaluatorDFA:
    def __init__(self):
        self.state = 'q0'
        self.final_states = {'q45'}

    def is_valid_letter(self, char):
        return char.isalpha()

    def is_valid_number(self, char):
        return char.isdigit()

    def transition(self, current_state, char):
        print(f"Transición: Estado actual: {current_state}, Carácter: {char}")

        if current_state == 'q0' and char == '(':
            return 'q1'
        
        elif current_state == 'q1' and char == '0':
            return 'q2'
        elif current_state == 'q2' and char == '1':
            return 'q3'
        elif current_state == 'q3' and char == ')':
            return 'q4'

        elif current_state in ['q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10', 'q11', 'q12', 'q13', 'q14', 'q15', 'q16'] and self.is_valid_number(char):
            return f'q{int(current_state[1:]) + 1}'

        elif current_state == 'q16' and char == '(':
            print(f"Iniciando segmento (17) desde el estado {current_state}")  
            return 'q17'

        elif current_state == 'q17' and char == '1':
            return 'q18'
        elif current_state == 'q18' and char == '7':
            return 'q19'
        elif current_state == 'q19' and char == ')':
            return 'q20'

        elif current_state == 'q20' and char in ['0', '1', '2']:
            return 'q21'
        elif current_state == 'q21' and char in ['0', '1', '2', '3']:
            return 'q22'
        elif current_state == 'q22' and char in ['0', '1', '2', '3']:
            return 'q23'

        elif current_state == 'q23' and char in ['0', '1']:
            return 'q24'
        elif current_state == 'q24' and char in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:  
            return 'q26'

        elif current_state == 'q26' and char == '(':
            return 'q27'

        elif current_state == 'q27' and char == '1':
            return 'q28'
        elif current_state == 'q28' and char == '0':
            return 'q29'
        elif current_state == 'q29' and char == ')':
            return 'q30'

        elif current_state in ['q30', 'q31', 'q32'] and (self.is_valid_letter(char) or self.is_valid_number(char)):
            return f'q{int(current_state[1:]) + 1}'

        elif current_state == 'q32':
            if self.is_valid_letter(char) or self.is_valid_number(char):
                return 'q40'
            else:
                return 'invalid'  # Asegura que no se avance en un estado inválido.

        elif current_state == 'q40' and char == '(':
            return 'q41'

        elif current_state == 'q41' and char == '3':
            return 'q42'
        elif current_state == 'q42' and char in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            return 'q43'
        
        elif current_state in ['q43', 'q44', 'q45'] and self.is_valid_number(char):
            return f'q{int(current_state[1:]) + 1}'
        
        elif current_state == 'q45' and self.is_valid_number(char):
            return 'q40'

        return 'invalid'

    def evaluate_gs1(self, code):
        self.state = 'q0'
        print(f"Evaluando código: {code}")
        
        for char in code:
            self.state = self.transition(self.state, char)
            if self.state == 'invalid':
                print("Código GS1-128 inválido")
                return False
        
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
code_to_evaluate = "(01)12345678901234(17)250229(10)LOT156(30)509"
result = GS1EvaluatorService.evaluate_code(code_to_evaluate)
print(result)
