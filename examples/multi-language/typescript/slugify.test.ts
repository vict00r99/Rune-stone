// Tests generated from: ../slugify.rune

import { slugify } from "./slugify";

// Basic slugification
test("simple text", () => {
  expect(slugify("Hello World")).toBe("hello-world");
});

test("multi word title", () => {
  expect(slugify("My Blog Post Title")).toBe("my-blog-post-title");
});

// Accented characters
test("french accents", () => {
  expect(slugify("Café Résumé")).toBe("cafe-resume");
});

test("spanish accents", () => {
  expect(slugify("Ñoño año")).toBe("nono-ano");
});

test("german accents", () => {
  expect(slugify("Ünïcödé")).toBe("unicode");
});

// Special characters
test("punctuation removed", () => {
  expect(slugify("Hello, World!")).toBe("hello-world");
});

test("symbols removed", () => {
  expect(slugify("price = $100")).toBe("price-100");
});

test("ampersand removed", () => {
  expect(slugify("foo & bar")).toBe("foo-bar");
});

// Whitespace handling
test("multiple spaces collapsed", () => {
  expect(slugify("  too   many   spaces  ")).toBe("too-many-spaces");
});

test("already slugged unchanged", () => {
  expect(slugify("already-slugged")).toBe("already-slugged");
});

// Edge cases
test("empty string", () => {
  expect(slugify("")).toBe("");
});

test("only special characters", () => {
  expect(slugify("!!!")).toBe("");
});

test("numbers preserved", () => {
  expect(slugify("123")).toBe("123");
});

// Custom separator
test("underscore separator", () => {
  expect(slugify("Hello World", "_")).toBe("hello_world");
});

test("dot separator", () => {
  expect(slugify("My Blog Post", ".")).toBe("my.blog.post");
});
