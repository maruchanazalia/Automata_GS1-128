import re
import csv


class GS1EvaluatorDFA:
    def __init__(self):
        self.pattern = r"\(01\)\d{14}\(17\)\d{6}\(10\)[A-Z]{3}\d{3}\(30\)\d{1,4}"

    def validate_code(self, gs1_code: str) -> str:
        """
        Valida un código GS1-128 completo y devuelve un mensaje sobre la validez.
        """
        gs1_code = gs1_code.replace(" ", "")  
        gs1_code = gs1_code.strip()  #BYEEE espacios 

        print("Validando código:", gs1_code)  # verificar SI IMPRIME EL CODIGO HAA

        if re.match(self.pattern, gs1_code):
            segment_errors = []
            
            if not self._validate_segment01(gs1_code):
                segment_errors.append("El segmento (01) debe contener exactamente 14 dígitos.")
            if not self._validate_segment17(gs1_code):
                segment_errors.append("El segmento (17) debe contener exactamente 6 dígitos y ser una fecha válida.")
            if not self._validate_segment10(gs1_code):
                segment_errors.append("El segmento (10) debe contener 3 letras seguidas de 3 números.")
            if not self._validate_segment30(gs1_code):
                segment_errors.append("El segmento (30) debe contener entre 1 y 3 dígitos y no exceder 999.")

            if segment_errors:
                return "Código inválido: " + ', '.join(segment_errors)

            return "Código válido."
        else:
            return "Código inválido: No coincide con el patrón."

    def _validate_segment01(self, gs1_code: str) -> bool:
        """Valida el segmento (01) para que contenga exactamente 14 dígitos."""
        segment01 = re.search(r"\(01\)(\d{14})", gs1_code)
        return segment01 is not None

    def _validate_segment17(self, gs1_code: str) -> bool:
        """Valida el segmento (17) para que contenga exactamente 6 dígitos."""
        segment17 = re.search(r"\(17\)(\d{6})", gs1_code)
        if segment17:
            return self._validate_date_segment(segment17.group(1))
        return False

    def _validate_segment10(self, gs1_code: str) -> bool:
        """Valida el segmento (10) para que contenga exactamente 3 letras seguidas de 3 números."""
        segment10 = re.search(r"\(10\)([A-Z]{3}\d{3})", gs1_code)
        if segment10:
            value = segment10.group(1)
            print(f"Segmento (10) encontrado: {value}")  
            if len(value) == 6: 
                return True
            print(f"Segmento (10) incorrecto: {value}")  
        return False

    def _validate_segment30(self, gs1_code: str) -> bool:
        """Valida el segmento (30) para que contenga entre 1 y 3 dígitos y que no exceda 999."""
        segment30 = re.search(r"\(30\)(\d{1,4})", gs1_code) 
        if segment30:
            value = segment30.group(1)
            if len(value) > 3:  
                print(f"Segmento (30) incorrecto: encontrado más de 3 dígitos: {value}")  
                return False  
            value = int(value)
            print(f"Segmento (30) encontrado: {value}") 
            if value > 999:
                return False  
            return 1 <= value <= 999  
        return False

    def _validate_date_segment(self, date_str: str) -> bool:
        """Valida el formato del segmento de fecha."""
        yy = int(date_str[:2])
        mm = int(date_str[2:4])
        dd = int(date_str[4:6])
        year = 2000 + yy  
        
        return (1 <= mm <= 12 and
                (mm in {1, 3, 5, 7, 8, 10, 12} and 1 <= dd <= 31 or
                 mm in {4, 6, 9, 11} and 1 <= dd <= 30 or
                 (mm == 2 and (self._is_leap_year(year) and 1 <= dd <= 29 or
                               not self._is_leap_year(year) and 1 <= dd <= 28))))

    def _is_leap_year(self, year: int) -> bool:
        """Determina si un año es bisiesto."""
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    def process(self, gs1_string: str) -> dict:
        """Procesa y valida la cadena GS1-128 completa y retorna un diccionario."""
        gs1_codes = gs1_string.splitlines()  # Separar por lineas los códigos dse cadena aaaaaaaaaa
        results = []
        for code in gs1_codes:
            result = self.validate_code(code)
            results.append(result)

        #csv
        with open('resultados_gs1.csv', mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Código GS1', 'Resultado'])  

                for code in gs1_codes:
                    result = self.validate_code(code)
                    results.append(result)
                    writer.writerow([code, result])


        # DEVUELME EL PERRO RESULTADO VAMOSSS
        if all("Código válido." in res for res in results):
            return {"status": "success", "message": "Todos los códigos son válidos."}
        else:
            return {"status": "error", "message": "Algunos códigos son inválidos.", "details": results}
