-- Check if the database exists, if not create it
CREATE DATABASE IF NOT EXISTS django_blog;
USE django_blog;

-- Check if the Post table exists, if not create it
CREATE TABLE IF NOT EXISTS Post (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100),
    content TEXT,
    author_id INT,
    FOREIGN KEY (author_id) REFERENCES auth_user(id) ON DELETE CASCADE
);

-- Check if the taggit_tag table exists, if not create it
CREATE TABLE IF NOT EXISTS taggit_tag (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) NOT NULL
);

-- Check if the taggit_taggeditem table exists, if not create it
CREATE TABLE IF NOT EXISTS taggit_taggeditem (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tag_id INT,
    content_type_id INT,
    object_id INT,
    FOREIGN KEY (tag_id) REFERENCES taggit_tag(id) ON DELETE CASCADE
);
