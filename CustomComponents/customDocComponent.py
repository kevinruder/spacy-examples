import spacy

# Define the custom component
def length_component(doc):
    # Get the doc's length
    doc_length = len(doc)  
    print("This document is {} tokens long.".format(doc_length))
    
    doc.set_extension('length', getter=lambda doc : len(doc))
    
    # Return the doc
    return doc


# Load the small English model
nlp = spacy.load("en_core_web_sm")


# Add the component first in the pipeline and print the pipe names
nlp.add_pipe(length_component, name="length", first=True)
print(nlp.pipe_names)

# Process a text
doc = nlp("some text is here, what's up ?")
print(doc._.length)