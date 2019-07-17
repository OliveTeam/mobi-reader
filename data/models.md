# Models for our JSON
## Common
```typescript
interface UniqueIdObject {
    id: string;                     // unique, automatic
    key: string;                    // unique
    label: string;
}
```
## Author
```typescript
interface Author extends UniqueIdObject{
    name: string;
    birthDate: string;
    deathDate: string;
}
```
## Book
```typescript
enum MainGenre {
    DRAMA = 'DRAMA',
    ESSAY = 'ESSAY',
    LETTER = 'LETTER',
    NOVEL = 'NOVEL',
    POETRY = 'POETRY'
}

enum SubGenre {
    ROMANCE_NOVEL = 'ROMANCE_NOVEL',
    ...
}

enum BookFormat {
    E_READER = 'E_READER',
    EPUB = 'EPUB',
    HTML = 'HTML',
    MOBI_POCKET = 'MOBI_POCKET',
    PDF = 'PDF',
    SONY_READER = 'SONY_READER'
    WORD = 'WORD',
}

interface BookFile {
    raw: {
        path: string;
        format: BookFormat;
    }[];                        // a book can be in multiple parts
    processed?: {
        path: string;           // path to clean txt, can be rebuilt from raw if needed
    }
}

interface Book extends UniqueIdObject {
    author: Author              // document reference (mongoDB) or ID (we can update author without changing all of his books)
    title: string;
    genre: MainGenre,
    subGenre: SubGenre,
    parutionDate: string;
    location: BookFile;
}
```