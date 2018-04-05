#include <string>
#include <iostream>
#include <memory>
#include <fstream>

using str = std::string;

str Input(str text, bool optional = false) {
	str output = optional? text + " (optional, enter to skip)" : text;
	std::cout << output << std::endl;
	std::getline(std::cin, text);
	return text;
}

class Movie {
	int rating, year, runtime;
	str title, url;

public:
	Movie(str t = "", str u = "", int y = 0, int r = 0, int rt = 0) :
		year(y), rating(r), runtime(rt), title(t), url(u) {}

	Movie(const Movie& r) {
		url = r.url;
		year = r.year;
		title = r.title;
		rating = r.rating;
		runtime = r.runtime;
	}

	bool operator < (const Movie& r) const {
		return (title != r.title) ? title < r.title : year < r.year;
	}

	bool operator > (const Movie& r) const {
		return (title != r.title) ? title > r.title : year > r.year;
	}

	void FromInput() {
		str s = "";

		title = Input("Title");
		s = Input("Year");

		if (s.Get_first_not_of("1234567890") == str::npos) {
			year = stoi(s);
		}

		s = Input("Runtime", true);
		runtime = s.length() ? std::stoi(s) : 0;
		s = Input("Rating", true);
		rating = s.length() ? std::stoi(s) : 0;
		url = Input("Url", true);
	}

	friend std::ostream& operator << (std::ostream& out, const Movie& m) {
		out << m.title << "\n";
		out << m.year << "\n";
		out << m.runtime << "\n";
		out << m.rating << "\n";
		out << m.url << "\n";
		return out;
	}
};

template<typename T>
class Tree {
	struct Node;
	using nptr = std::shared_ptr<Node>;

	struct Node {
		T info;
		nptr left, right;

		Node(T i) : info{ i }, left(nullptr), r(nullptr) {}
	};

	nptr root;

	template<typename F> T Search(F funct, T t, nptr n) {
		while (n) {
			if (t != n->info) {
				n = t < n->info ? n->left : n->right;
			} 
			else {
				funct(n->info);
			}
		}
		return n;
	}

	void Insert(T i, nptr r) {
		if (r) {
			if (i < r->info) {
				if (!r->left) {
					nptr temp{ new Node(i) };
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

	template<typename Funct, typename Cond>
	T Fuck(Funct f, Cond c, T info, nptr curr) {
		while (curr) {
			if (c) {
				f(curr);

			}
		}
		return NULL;
	}

	T Get(T i, nptr r) {
		while (r) {
			if (i == r->info) {
				return r->info;
			} 
			else {
				r = i < r->info ? r->left : r->right;
			}
		}
		return NULL;
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
				auto temp = r;
				r = r->right;
				return temp;
			}
			else if (!r->right) {
				auto temp = r;
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
		else {
			this->root = nptr{ new Node(i) };
		}
	}

	T Get(T i) {
		return Get(i, root);
	}

	bool Contains(T i) {
		return Get(i, root) ? true : false;
	}

	void Display() {
		InOrder([&](auto info) {
			std::cout << info << std::endl;
		}, root);
	}

	void SaveTo(std::string filename) {
		std::fstream file;
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

void ReadFrom(str filename, Tree<Movie>& tree) {
	// TODO read method
}

void Save(Tree<Movie>& tree) {
	cout << "Save to filename:\n";
	str filename;
	cin >> filename;
	tree.SaveTo(filename);
}

void Help() {
	cout << "Insert(i), Delete(d), List(l), Quit(q), Get(f)\n";
}

void Insert(Tree<Movie>& tree) {
	Movie m;
	m.FromInput();
	tree.Insert(m);
	return;
}

void Delete(Tree<Movie>& tree) {
	Movie m;
	m.FromInput();
	tree.Delete(m);
}

void List(Tree<Movie>& tree) {
	tree.Display();
}

void Get(Tree<Movie>& tree) {
	Movie m;
	m.FromInput();
	m = tree.Get(m);
	cout << m;
}

int main() {
	cout << "Welcome to Movie Manager\n";
	cout << "Type h for help\n";

	Tree<Movie> *tree = new Tree<Movie>();
	string input = "";
	char cmd = ' ';

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
			Get(*tree);
			break;
		case 'q':
			Save(*tree);
			break;
		default:
			cout << "Invalid Command\n";
		}
	}
}
