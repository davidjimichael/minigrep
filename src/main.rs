fn main() {
    let args: Vec<_> = std::env::args().collect();
    if args.len() < 3 {
        eprintln!("ERROR: expected input -> cargo run \"<message>\" <encode|decode>");
        return;
    }

    let text = &args[2];
    let action = &args[1];
    
    if action == "encode" {
        let _res = encode(text);
        println!("Encoded \"{}\":\n{}", text, _res);
    }
    else if action == "decode" {
        let _res = decode(text);
        println!("Decoded \"{}\":\n{}", text, _res);
    }
    else {
        println!("Unrecognized command");
    }
}

fn encode(plaintext: &str) -> String {
    let ciphertext: String = plaintext.chars().map(|c| encode_char(c).to_string()).collect();
    ciphertext.trim_right().to_string()
}

pub fn decode(ciphertext: &str) -> String {
    ciphertext.split_whitespace().map(|w| decode_cipher_char(w)).collect()
}

// todo: create bsts for chars and codes to prevent the classic copy pasterino here
pub fn encode_char(letter: char) -> &'static str {
    let mut _letter = letter.clone();
    _letter.make_ascii_uppercase();

    match _letter {
        'A' =>	"·−",
        'B' =>	"−···",
        'C' =>	"−·−·",
        'D' =>	"−·· ",
        'E' =>	"·",
        'F' =>	"··−·", 	 	 	
        'G' =>	"−−· ",	 	            
        'H' =>	"····",		 	  	    
        'I' =>	"··",
        'J' =>	"·−−−",
        'K' =>	"−·− ",
        'L' =>	"·−··",
        'M' =>	"−−",
        'N' =>	"−·",
        'O' =>	"−−−",
        'P' =>	"·−−·",
        'Q' =>	"−−·−",
        'R' =>	"·−·",
        'S' =>	"···",
        'T' =>	"−",
        'U' =>	"··−",
        'V' =>	"···−",
        'W' =>	"·−−",
        'X' =>	"−··−",
        'Y' =>	"−·−−",
        'Z' =>	"−−··",
        '0' =>	"−−−−−",
        '1' =>	"·−−−−",
        '2' =>	"··−−−",
        '3' =>	"···−−",
        '4' =>	"····−",
        '5' =>	"·····",
        '6' =>	"−····",
        '7' =>	"−−···",
        '8' =>	"−−−··",
        '9' =>	"−−−−·",
        ' ' | '\t' | '\n' => " ",	  	        
        _ => panic!("Decode error: Non ascii alphanumeric")
    }
}

pub fn decode_cipher_char(cipher: &str) -> char {
    match cipher {
        "·−" => 'A',    
        "−···" => 'B', 
        "−·−·" => 'C',
        "−·· " => 'D',
        "·" => 'E',
        "··−·" => 'F', 	 	 	
        "−−· " => 'G',	            
        "····" => 'H',	 	  	    
        "··" => 'I',
        "·−−−" => 'J',
        "−·− " => 'K',
        "·−··" => 'L',
        "−−" => 'M',
        "−·" => 'N',
        "−−−" => 'O',
        "·−−·" => 'P',
        "−−·−" => 'Q',
        "·−·" => 'R',
        "···" => 'S',
        "−" => 'T',
        "··−" => 'U',
        "···−" => 'V',
        "·−−" => 'W',
        "−··−" => 'X',
        "−·−−" => 'Y',
        "−−··" => 'Z',
        "−−−−−" => '0',
        "·−−−−" => '1',
        "··−−−" => '2',
        "···−−" => '3',
        "····−" => '4',
        "·····" => '5',
        "−····" => '6',
        "−−···" => '7',
        "−−−··" => '8',
        "−−−−·" => '9',
        " " | "\t" | "\n" => ' ',
        _ => panic!("Encode error: Non ascii alphanumeric")
    }
}

#[test]
fn encoding() {
    let plainttext = "Firefox";
    let expected = "··−····−····−·−−−−··−";
    let result = encode(plainttext);
    
    assert_eq!(expected, &result);
}

#[test]
fn decoding() {
    let ciphertext = "··−· ·· ·−· · ··−· −−− −··−";
    let expected = "FIREFOX";
    let result = decode(ciphertext);
    
    assert_eq!(expected, &result);
}
