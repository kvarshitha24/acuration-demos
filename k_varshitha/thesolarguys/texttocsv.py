import csv

# Function to split the text into question-answer pairs
def split_text_into_pairs(text):
    pairs = []
    current_pair = {"question": "", "answer": ""}
    lines = text.strip().split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            # Check if the current pair has both question and answer
            if current_pair["question"] and current_pair["answer"]:
                pairs.append(current_pair)
            current_pair = {"question": "", "answer": ""}
        elif current_pair["question"] == "":
            current_pair["question"] = line
        else:
            current_pair["answer"] += line + " "
    # Append the last pair if it's not empty
    if current_pair["question"] and current_pair["answer"]:
        pairs.append(current_pair)
    return pairs

# Function to write pairs into CSV file
def write_to_csv(pairs, filename):
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Question", "Answer"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for pair in pairs:
            writer.writerow({"Question": pair["question"], "Answer": pair["answer"]})

# Read text data from file
def read_text_from_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()

# Your file name containing the text data
filename = "/content/final_the solar guys (1).txt"

# Read text data from file
text_data = read_text_from_file(filename)

# Split text into question-answer pairs
pairs = split_text_into_pairs(text_data)

# Write pairs into CSV file
write_to_csv(pairs, "solar_guys_qa.csv")
