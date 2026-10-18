class MealyMachine:
    def __init__(self):
        # Initial state
        self.current_state = 'q0'
        
        # State transitions and outputs: (current_state, symbol) -> (next_state, output)
        self.transitions = {
            # Start State (q0)
            ('q0', '/'): ('q1', 0),
            ('q0', 'a'): ('q_trap', 0),
            ('q0', '*'): ('q_trap', 0),
            
            # Saw '/' (q1)
            ('q1', '*'): ('q2', 0),
            ('q1', 'a'): ('q_trap', 0),
            ('q1', '/'): ('q_trap', 0),
            
            # Inside Comment (q2)
            ('q2', 'a'): ('q2', 0),
            ('q2', '/'): ('q2', 0),
            ('q2', '*'): ('q3', 0),
            
            # Got '*' Inside Comment (q3)
            ('q3', '*'): ('q3', 0),
            ('q3', 'a'): ('q2', 0),
            ('q3', '/'): ('q4', 1),  # Output 1 indicates comment closed properly
            
            # Comment Closed State (q4) - Any extra characters after closure go to trap
            ('q4', 'a'): ('q_trap', 0),
            ('q4', '*'): ('q_trap', 0),
            ('q4', '/'): ('q_trap', 0),
            
            # Trap State (q_trap)
            ('q_trap', 'a'): ('q_trap', 0),
            ('q_trap', '*'): ('q_trap', 0),
            ('q_trap', '/'): ('q_trap', 0),
        }

    def process_string(self, input_string):
        """Processes an input string character by character through the Mealy machine."""
        self.current_state = 'q0'  # Reset state
        state_history = [self.current_state]
        outputs = []

        for symbol in input_string:
            # Map any character that is not '*' or '/' to 'a' as specified in the rules
            mapped_symbol = symbol if symbol in ['*', '/'] else 'a'

            if (self.current_state, mapped_symbol) in self.transitions:
                next_state, output = self.transitions[(self.current_state, mapped_symbol)]
                outputs.append(output)
                self.current_state = next_state
                state_history.append(next_state)

        # String is accepted if the machine reached q4 and emitted 1 on the final character
        is_accepted = (self.current_state == 'q4') and (outputs[-1] == 1 if outputs else False)
        
        return state_history, outputs, is_accepted


if __name__ == "__main__":
    mealy = MealyMachine()

    # Prompt user for input
    user_input = input("Enter a C-style comment string to test: ").strip()

    if user_input:
        states, outputs, accepted = mealy.process_string(user_input)

        print("\n--- Processing Results ---")
        print(f"Input String  : {user_input}")
        print(f"State Sequence: {' -> '.join(states)}")
        print(f"Outputs       : {outputs}")
        print(f"Result        : {'ACCEPTED!' if accepted else 'REJECTED!'}")
    else:
        print("No input provided.")