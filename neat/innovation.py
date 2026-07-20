

class InnovationTracker:
    
    def __init__(self, start_number=0):
        """
        Initialize the innovation tracker.
        
        Args:
            start_number: The initial value for the global counter (default: 0).
                         The first innovation will be start_number + 1.
        """
        self.global_counter = start_number
        self.generation_innovations = {}
    
    def get_innovation_number(self, input_node, output_node, mutation_type='add_connection'):
        pass
    
    def reset_generation(self):
        pass
    
    def get_current_innovation_number(self):
        pass
    
    def __repr__(self):
        return (f"InnovationTracker(global_counter={self.global_counter}, "
                f"generation_innovations={len(self.generation_innovations)} tracked)")
    
    def __getstate__(self):
        """
        Prepare tracker for pickling (checkpoint save).
        
        Returns a dictionary containing the state to be pickled.
        """
        return {
            'global_counter': self.global_counter,
            'generation_innovations': self.generation_innovations.copy()
        }
    
    def __setstate__(self, state):
        """
        Restore tracker from pickled state (checkpoint restore).
        
        Args:
            state: Dictionary containing the pickled state
        """
        self.global_counter = state['global_counter']
        self.generation_innovations = state['generation_innovations']
