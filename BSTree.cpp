#include <string>
#include <iostream>
#include <memory>
#include <fstream>

using str = std::string;

str Input(str text, bool optional = false) {
	str output = !optional ? text : text + " (optional, enter to skip)";
	std::cout <<  output << std::endl;
	std::getline(std::cin, text);
	return text;
}

bool isNum(str numstr) {
    return numstr.find_first_not_of("0123456789") == str::npos;
}
        
int parse(str numstr) {
    return isNum(numstr) ? std::stoi(numstr) : 0;
}

class Movie {
	int rating, year, runtime;
	str title, url;

public:
	Movie(str t = "", str u = "", int y = 0, int r = 0, int rt = 0) :
		year(y), rating(r), runtime(rt), title(t), url(u) {}

	Movie(const Movie &r)
	{
		url = r.url;
		year = r.year;
		title = r.title;
		rating = r.rating;
		runtime = r.runtime;
	}
	
	void Title(str t) { title = t; }
    void Year(int y) { year = y; }
    void Rating(int r) { rating = r; } 
    void Runtime(int r) { runtime = r; }
    void Url(str u) { url = u; }
    
	bool operator < (const Movie &r) const {
		return (title != r.title) ? title < r.title : year < r.year;
	}

	bool operator > (const Movie &r) const {
		return (title != r.title) ? title > r.title : year > r.year;
	}

	void FromInput() {
        while (title == "" && year == 0) {
            title = Input("Title");
		    year  = parse(Input("Year"));
        }
		runtime = parse(Input("Runtime", true));
		rating  = parse(Input("Rating", true));
		url     = Input("Url", true);
	}

	friend std::ostream& operator << (std::ostream &out, const Movie &m) {
		return out 
		    << m.title   << "\n"
		    << m.year    << "\n"
		    << m.runtime << "\n"
		    << m.rating  << "\n"
		    << m.url     << "\n";
	}
};

template<typename T>
class Tree {
	struct Node;
	using nptr = std::shared_ptr<Node>;

	struct Node {
		T info;
		nptr left, right;

		Node(T i = NULL, nptr l = nullptr, nptr r = nullptr) :
			info(i), left(l), right(r) {}
	};

	nptr root;
	
	void Insert(T i, nptr r) {
		if (r) {
			if (i < r->info) {
				if (!r->left) {
					nptr temp { new Node(i) };
					r->left = temp;
				} 
				else {
					Insert(i, r->left);
				}
			}
			else {
				if (!r->right) {
					nptr temp{ new Node(i) };
					r->right = temp;
				}
				else {
					Insert(i, r->right);
				}
			}
		}
	}

	T Find(T i, nptr r) {
		while (r) {
			if (i < r->info) {
				r = r->left;
			}
			else if (i > r->info) {
				r = r->right;
			}
			else {
				return r->info;
			}
		}
		return *new T();
	}

	template<typename F>
	void InOrder(F f, nptr r) {
		if (!r) return;
		InOrder(f, r->left);
		f(r->info);
		InOrder(f, r->right);
	}
	
	template<typename F>
	void PreOrder(F f, nptr r) {
		if (!r) return;
		f(r->info);
		InOrder(f, r->left);
		InOrder(f, r->right);
	}

	nptr Delete(T t, nptr r) {
		if (!r) {
			return r;
		}
		if (t < r->info) {
			r->left = Delete(t, r->left);
		}
		else if (t > r->info) {
			r->right = Delete(t, r->right);
		}
		else {
			if (!r->left) {
				nptr temp = r;
				r = r->right;
				return temp;
			}
			else if (!r->right) {
				nptr temp = r;
				r = r->left;
				return temp;
			}
			else {
				nptr temp = r->right;

				while (temp->left) {
					temp = temp->left;
				}

				r->info = temp->info;
				r->right = Delete(temp->info, r->right);
			}
			return r;
		}
	}

public:
	Tree() : root{ nullptr } {}
	
	T Delete(T i) {
		return Delete(i, root)->info;
	}

	void Insert(T i) {
		if (root) {
			return Insert(i, root);
		}
		this->root = nptr{ new Node(i) };
	}

	T Find(T i) {
		return Find(i, root);
	}

	bool Contains(T i) {
		return Find(i, root) ? true : false;
	}
	
	void Display() {
		InOrder([&](auto info){ 
			std::cout << info << std::endl;
		}, root);
	}

	void SaveTo(std::string filename) {
		std::ofstream file;
		file.open(filename);

		if (file.is_open()) {
			PreOrder([&](auto info) {
				file << info;
			}, root);
			file.close();
		}
	}
};

using namespace std; // lots of couts in the next stage 

void ReadFrom(str filename, Tree<Movie> &tree) {
	std::ifstream file;
	file.open(filename);
    Movie m;
    str s = "";
    
	if (file.is_open()) {
	    while (file >> s) {
            m.Title(s);
            getline(file, s); 
            m.Year(parse(s));
            file >> s;
            m.Runtime(parse(s));
            file >> s;
            m.Rating(parse(s));
            file >> s;
            m.Url(s);
            tree.Insert(m);
        }
		file.close();
	}
}

void Save(Tree<Movie> &tree) {
	tree.SaveTo(Input("Save to filename"));
}

void Help() {
	cout << "Insert(i), Delete(d), List(l), Quit(q), Find(f)\n";
}

void Insert(Tree<Movie> &tree) {
	Movie m;
	m.FromInput();
	tree.Insert(m);
	return;
}

void Delete(Tree<Movie> &tree) {
	Movie m;
	m.FromInput();
	tree.Delete(m);
}

void List(Tree<Movie>& tree) {
	tree.Display();
}

void Find(Tree<Movie> &tree) {
	Movie m;
	m.FromInput();
	m = tree.Find(m);
	cout << m;
}

int main() {
	cout << "Welcome to Movie Manager\n";
	cout << "Type h for help\n";

	Tree<Movie> *tree = new Tree<Movie>();
	string input = "";
	char cmd = ' ';

	ReadFrom(Input("Load file"), *tree);

	while (cmd != 'q') {
		input = Input("Command");
		cmd = tolower(input[0]);

		switch (cmd) {
		case 'h':
			Help();
			break;
		case 'l':
			List(*tree);
			break;
		case 'i':
			Insert(*tree);
			break;
		case 'd':
			Delete(*tree);
			break;
		case 'f':
			Find(*tree);
			break;
		case 'q':
			Save(*tree);
			break;
		default:
			cout << "Invalid Command\n";
		}
	}
}