// /src/cchars.rs
// functions to handle cipher/decipher of char

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
        " " => ' ',
        _ => panic!("Encode error: Non ascii alphanumeric")
    }
}