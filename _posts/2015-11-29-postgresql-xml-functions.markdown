---
layout: post
title:  "PostgreSQL XML Functions"
date:   2015-11-29 20:59:23
categories: postgresql xml function xmlagg xmlforest wordpress
---

Recently I needed to create XML straight from a relational database.
The use case was to create an import file for [Wordpress][wordpress] (WRX)
without writing any line of Python or Ruby code.
The legacy blogging application was using a [PostgreSQL][postgresql] database
that holds: users/authors, articles, comments and some other relations.

It's not the intention to describe the whole process here.
Much more, it attempts to make it adaptable to other situations.

#### Importing users/authors (no aggregation)

The easiest case was the users table without any relations and no need for
aggregation. The goal was to create XML elements like this:

{% highlight xml %}
<wp:author>
  <wp:author_id>1</wp:author_id>
  <wp:author_login>stefan</wp:author_login>
  <wp:author_email>stefan@example.com</wp:author_email>
  <wp:display_name>Stefan</wp:display_name>
  <wp:first_name>Stefan</wp:first_name>
  <wp:last_name>Jenkner</wp:last_name>
</wp:author>
{% endhighlight %}

This can be done with this select statement:

{% highlight sql %}
SELECT xmlelement(
    name "wp:author",
        xmlforest (
          id as "wp:author_id",
          username as "wp:author_login",
          email as "wp:author_email",
          first_name as "wp:display_name",
          first_name as "wp:first_name",
          last_name as "wp:last_name"
          )
        )
FROM users ORDER BY id;
{% endhighlight %}

The `xmlelement` expression produces an XML element with the name *wp:author*.
Then instead of nesting six other `xmlelement` statements (for *id*, *username*,
...), it was easier (and even more readable) to make use of the `xmlforest`
expression and create a sequence of the given elements.

#### Articles and comments (covering XML aggregation)

The goal was to create XML elements like this. An item can have none or
multiple comments:

{% highlight xml %}
<item>
  <title>PostgreSQL rocks!</title>
  <link>http://example.com/blog/2013/06/18/postgresql-rocks/</link>
  <pubDate>2013-06-18T10:53:25+00:00</pubDate>
  <dc:creator>stefan</dc:creator>
  <guid>http://example.com/?p=99</guid>
  <description/>
  <content:encoded>...</content:encoded>
  <excerpt:encoded>...</excerpt:encoded>
  <wp:post_id>99</wp:post_id>
  <!-- ... -->
  <wp:post_date>2013-06-18T10:53:25+00:00</wp:post_date>
  <!-- first comment -->
  <wp:comment>
    <wp:comment_id>551</wp:comment_id>
    <wp:comment_author>guest1</wp:comment_author>
    <wp:comment_author_email>guest1@example.com</wp:comment_author_email>
    <!-- ... -->
    <wp:comment_content>I like it!</wp:comment_content>
    <wp:comment_approved>1</wp:comment_approved>
  </wp:comment>
  <!-- next comment -->
  <wp:comment>
    <wp:comment_id>552</wp:comment_id>
    <!-- ... -->
  </wp:comment>
</item>
{% endhighlight %}

It is necessary to use a `LEFT JOIN` on comments and
`GROUP BY p.id` (ID of the article) to also include articles without comments.
To make it clear - the second column (count) of the following select statement can be zero:

{% highlight sql %}
SELECT p.id, COUNT(c.id)
FROM posts p
  LEFT JOIN comments c ON c.post_id = p.id
GROUP BY p.id
ORDER BY p.id;
{% endhighlight %}

Basically, the first part of the final statement is identical to the first
example. The `xmlelement` expression creates the *item* node and the
`xmlforest` expression creates it's children.

The `xmlagg` expression expects an XML element at the first argument.
It just concatenates the elements created by the `xmlelement` expression
and passes it to the aggregation call.

{% highlight sql %}
SELECT xmlelement(
    name item,
        xmlforest (
            p.title as "title",
            'http://example.com/blog/' || to_char(date, 'YYYY') || '/' || to_char(date, 'MM') || '/' || to_char(date, 'DD') || '/' || p.slug as "link",
            p.date as "pubDate",
            (SELECT username FROM users u WHERE u.id = p.author_id) as "dc:creator",
            'http://example.com/?p=' || p.id  as "guid",
            '' as "description",
            p.body as "content:encoded",
            p.excerpt as "excerpt:encoded",
            p.id as "wp:post_id",
            -- ... skipped
            date as "wp:post_date"
        ),
        xmlagg(
            xmlelement(
                name "wp:comment",
                xmlforest(
                    c.id as "wp:comment_id",
                    c.user_name as "wp:comment_author",
                    c.user_email as "wp:comment_author_email",
                    -- skipped ...
                    c.comment as "wp:comment_content",
                    c.id / c.id as "wp:comment_approved" -- '1'
                )
            )
        )
    )
FROM posts p
  LEFT JOIN comments c ON c.post_id = p.id
GROUP BY p.id
ORDER BY p.id;
{% endhighlight %}


I had some unexpected results when using constants like '1' or '0' within
the `xmlagg` functions. The following node was generated, even if an
article does not have any comments.

{% highlight xml %}
<wp:comment>
  <wp:wp:comment_approved>1</wp:wp:comment_approved>
</wp:comment>
</item>
{% endhighlight %}

The solution was to express '0' and '1' by using the comment's ID:

{% highlight sql %}
c.id - c.id as "wp:comment_parent" -- '0'
c.id / c.id as "wp:comment_approved" -- '1'
{% endhighlight %}


#### Further information

For additional information on [PostgreSQL][postgresql]'s XML functions,
check out [this section](https://en.wikipedia.org/wiki/PostgreSQL) of
the manual.




[postgresql]: https://www.postgresql.org
[wordpress]: https://www.wordpress.com
