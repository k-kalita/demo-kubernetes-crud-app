
CREATE TABLE IF NOT EXISTS `User` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `username` varchar(255) UNIQUE NOT NULL,
    `password_hash` varchar(64) NOT NULL,
    `name` varchar(255) NULL,
    `last_name` varchar(255) NULL,
    `email` varchar(255) UNIQUE NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;


CREATE TABLE IF NOT EXISTS `Post` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `title` varchar(255) NOT NULL,
    `content` text NOT NULL,
    `author_id` int(11) NOT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`author_id`) REFERENCES `User` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;


CREATE VIEW user_posts AS
    SELECT
        u.id AS user_id,
        u.username AS username,
        u.name AS name,
        u.email AS email,
        p.id AS post_id,
        p.title AS post_title,
        p.content AS post_content
    FROM User u
    LEFT JOIN Post p ON u.id = p.author_id;
