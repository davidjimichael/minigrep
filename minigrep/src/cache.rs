// /src/cache.rs

pub struct Cacher<F> where F: Fn(u32) -> u32 {
    funct: F,
    value: Option<u32>,
}

impl<F> Cacher<F> where F: Fn(u32) -> u32 {
    pub fn new(funct: F) -> Cacher<F> {
        Cacher {
            funct,
            value: None,
        }
    }

    pub fn value(&mut self, arg: u32) -> u32 {
        match self.value {
            Some(v) => v,
            None => {
                let v = (self.funct)(arg);
                self.value = Some(v);
                v
            },
        }
    }
}
