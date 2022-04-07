
def textlog(log_name: str = "error_log", path: str = ".") -> object:
    """
    Decorator responsable to save a log.txt file contaning he error of the funcition

    Args:
        log_name (str, optional): Name of the log file. Defaults to "error_log".
        path (str, optional): path of the log file. Defaults to ".".
    """
    def higher_wrapper(func: object) -> object:
        def wrapper(*args, **kwargs):
            from traceback import format_exc
            try:
                func(*args, **kwargs)
                
            except Exception:
                error = format_exc()
                with open(f"{path}/{log_name}.txt", "wt") as file:
                    file.writelines(error)       
        return wrapper
    return higher_wrapper

def time_counter(re_run: int):
    """
    Decorator para contar o tempo de execução de uma função.

    Args:
        re_run (int): Número de vezes que a função irá ser testada

    Returns:
        object: função original com a média de tempo entre o total de re_run
    """
    from statistics import mean
    from time import perf_counter
    
    def higher_wrapper(function: object) -> object:
        def wrapper(*args, **kwargs) -> object:
            
            count = []
            for i in range(re_run):
                start = perf_counter()
                func = function(*args, **kwargs)
                end = perf_counter()
                count.append(end - start)
                
            time = mean(count)
            
            print(f"Tempo de execução da função ({i + 1} re-runs): {time} segundos.")
            return func          
        return wrapper
    return higher_wrapper

def scroll_to_element(times:int=10) -> object:
    """
    Decorator para que, em caso de certeza que o elemento HTML está na página, usar a barra de scroll
    até o elemento ficar visível.

    Args:
        times (int, optional): Quantidade de vezes que usará a barra de scroll. Defaults to 10.

    Returns:
        object: Elemento do selenium ou None caso não ache nada
    """
    from selenium.common.exceptions import ElementClickInterceptedException, StaleElementReferenceException, TimeoutException
    from selenium.webdriver import Chrome
    def higher_wrapper(funcion: object) -> object:
        
        def wrapper(driver: Chrome):
            element = None
            i = 0
            while i <= times:
                driver.execute_script(f"window.scrollTo(0, 1)")
                try:
                    driver.execute_script(f"window.scrollTo(0, {100*i})")
                    
                    element =  funcion(driver) 
                    i += times
                     
                except (ElementClickInterceptedException, StaleElementReferenceException, TimeoutException):
                    i += 1
            if element == None:
                raise TypeError("Selenium Element not found!")
                
            return element                 
        return wrapper
    return higher_wrapper

def merge_list(*args, unique: bool = False, tupla: bool = False) -> list:
    """
    Função para mesclar/concatonat listas.

    Returns:
        list: Lista com o resultado da mesclagem
    """
    data = []
    for arg in args:
        data += arg
        
    if unique:    
        data = list(set(data))
    if tupla:
        data = tuple(data)
        
    return data

class Encrypt:
    
    def __init__(self, language: dict = None):
       
        import random
        
        letter_lower = "abcdefghijklmnopqrstuvwxyz"
        letter_upper = letter_lower.upper()
        other_letters_lower = "çáãéêâîíõôóúàèìòùú'"
        other_letters_upper = other_letters_lower.upper()
        numbers = "0123456789"
        symbols = r'\/?°´ª[{]}-+=§!@#$%¨&*()$£¢¬º^~:;.<>,| "'

        characteres = letter_lower + letter_upper + numbers + symbols + other_letters_lower + other_letters_upper
        
        if language:
            self.encripytion_language = language
        else:
            self.encripytion_language = {key:" " for key in characteres }
            
            for value in self.encripytion_language: 
                while True:
                    letter = "".join(random.choices(characteres, k=2))
                    if letter not in self.encripytion_language.values():
                        self.encripytion_language[value] = letter
                        break
            self.encripytion_language.update({"\n": "\n"+ random.choice(characteres)})       
        
    def encrypt(self, message: str) -> str:    
        """
        Encripta a mensagem inserida pelo usuário

        Args:
            message (str): mensagem original

        Returns:
            str: mensagem encriptada de acordo com a linguagem definida para essa classe
        """
        
        encrypted_message_list = [self.encripytion_language[letter] for letter in message]
        
        return "".join(encrypted_message_list)

    def decrypt(self, message: str) -> str:
        """
        Decripta a mensagem inserida pelo usuário

        Args:
            message (str): mensagem encripdada para decriptar

        Raises:
            ValueError: levanta erro caso alguma letra do texto encriptadonão esteja na lista de letras da linuagem definida na classe

        Returns:
            str: mensagem decriptada de acordo com a linguagem definida para essa classe
        """
        
        original, encrypted = [value for value in self.encripytion_language.keys()], [value for value in self.encripytion_language.values()]
        encrypted_message_list = [message[i:i + 2] for i in range(0, len(message)) if i%2 == 0]

        decrypted_message_list = []
        for value in encrypted_message_list:
            try:
                index = encrypted.index(value)
            except ValueError:
                raise ValueError("Letter not on list, you are not using correct language!")
            decrypted_message_list.append(original[index])
    
        return "".join(decrypted_message_list)
    
    def __str__(self):
        print("Language dict {original character: encrypted character}: ",self.encripytion_language)
        
def verify_string(list_to_verify: list[str], string_to_verify: str) -> bool:
    """
    Function to verify if any of the values in the list is on string

    Args:
        list_to_verify (list): List of strings to verify
        string_to_verify (str): string to compare

    Returns:
        bool: True if any name of the list is in string, False otherwise.
    """
    boolean = False
    for value in list_to_verify:
        if value in string_to_verify:
            boolean = True
    return boolean

def is_word_similar(word:str, word_to_compare: str) -> bool:
    """
    Function to detect if word is similar based on parameters

    Args:
        word (str): original word 
        word_to_compare (str): word to be compared

    Returns:
        bool: True if word is similar, False otherwise
    """
    count = []
    if len(word_to_compare) - len(word) < 3:
        for letter, letter_to_compare in zip(word, word_to_compare):
            if letter_to_compare == letter:
                count.append(1)
            else:
                count.append(0.1)
        return True if sum(count) > len(word_to_compare)/1.2 else False

    return False

