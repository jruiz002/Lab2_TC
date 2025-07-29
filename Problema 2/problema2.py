class Stack:
    """Implementación de una pila para balancear expresiones"""
    
    def __init__(self):
        self.items = []
    
    def push(self, item):
        """Agregar elemento a la pila"""
        self.items.append(item)
    
    def pop(self):
        """Remover y retornar el elemento superior de la pila"""
        if not self.is_empty():
            return self.items.pop()
        return None
    
    def peek(self):
        """Ver el elemento superior sin removerlo"""
        if not self.is_empty():
            return self.items[-1]
        return None
    
    def is_empty(self):
        """Verificar si la pila está vacía"""
        return len(self.items) == 0
    
    def size(self):
        """Retornar el tamaño de la pila"""
        return len(self.items)
    
    def get_items(self):
        """Retornar todos los elementos de la pila como lista"""
        return self.items.copy()


def is_balanced(expression):
    """
    Verifica si una expresión está balanceada usando una pila.
    Retorna (bool, list) - (está_balanceada, pasos_de_la_pila)
    """
    stack = Stack()
    steps = []
    
    # Definir pares de símbolos que deben balancearse
    opening_symbols = {'(', '[', '{'}
    closing_symbols = {')', ']', '}'}
    symbol_pairs = {')': '(', ']': '[', '}': '{'}
    
    for i, char in enumerate(expression):
        step_info = {
            'position': i,
            'character': char,
            'action': '',
            'stack_before': stack.get_items(),
            'stack_after': []
        }
        
        if char in opening_symbols:
            # Es un símbolo de apertura
            stack.push(char)
            step_info['action'] = f"PUSH '{char}' - Símbolo de apertura"
            step_info['stack_after'] = stack.get_items()
            
        elif char in closing_symbols:
            # Es un símbolo de cierre
            if stack.is_empty():
                step_info['action'] = f"ERROR - Símbolo de cierre '{char}' sin símbolo de apertura correspondiente"
                step_info['stack_after'] = stack.get_items()
                steps.append(step_info)
                return False, steps
            
            top = stack.pop()
            if top != symbol_pairs[char]:
                step_info['action'] = f"ERROR - Símbolo de cierre '{char}' no coincide con '{top}'"
                step_info['stack_after'] = stack.get_items()
                steps.append(step_info)
                return False, steps
            
            step_info['action'] = f"POP '{top}' - Coincide con '{char}'"
            step_info['stack_after'] = stack.get_items()
        
        else:
            # Otro carácter (letras, operadores, etc.)
            step_info['action'] = f"Ignorar '{char}' - No es símbolo de balanceo"
            step_info['stack_after'] = stack.get_items()
        
        steps.append(step_info)
    
    # Verificar si quedan símbolos sin cerrar
    if not stack.is_empty():
        remaining = stack.get_items()
        step_info = {
            'position': len(expression),
            'character': 'END',
            'action': f"ERROR - Símbolos sin cerrar: {remaining}",
            'stack_before': remaining,
            'stack_after': []
        }
        steps.append(step_info)
        return False, steps
    
    return True, steps


def print_analysis(expression, is_balanced_result, steps):
    """Imprime el análisis detallado de una expresión"""
    print("=" * 80)
    print(f"EXPRESIÓN: {expression}")
    print("=" * 80)
    
    if is_balanced_result:
        print("✅ RESULTADO: La expresión está BIEN BALANCEADA")
    else:
        print("❌ RESULTADO: La expresión NO está balanceada")
    
    print("\n SECUENCIA DE PASOS DE LA PILA:")
    print("-" * 80)
    
    for i, step in enumerate(steps):
        print(f"Paso {i+1:2d} | Pos {step['position']:2d} | Char: '{step['character']}'")
        print(f"         | Acción: {step['action']}")
        print(f"         | Pila antes:  {step['stack_before']}")
        print(f"         | Pila después: {step['stack_after']}")
        print("-" * 80)
    
    print()


def main():
    """Función principal que lee el archivo y procesa cada línea"""
    filename = "ejercicios.txt"
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        print("ALGORITMO DE BALANCEO DE EXPRESIONES REGULARES")
        print("=" * 80)
        print(f"📁 Archivo procesado: {filename}")
        print(f"📄 Total de líneas: {len(lines)}")
        print("=" * 80)
        print()
        
        for line_num, line in enumerate(lines, 1):
            # Limpiar la línea de espacios en blanco y saltos de línea
            expression = line.strip()
            
            if expression:  # Solo procesar líneas no vacías
                print(f"📝 LÍNEA {line_num}:")
                is_balanced_result, steps = is_balanced(expression)
                print_analysis(expression, is_balanced_result, steps)
        
        print("ANÁLISIS COMPLETADO")
        
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo '{filename}'")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")


if __name__ == "__main__":
    main()
