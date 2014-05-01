---
layout: post
title:  "Howto migrate from Octopress to Jekyll"
date:   2014-05-01 14:11:52
categories: jekyll octropress
---

Here are a few tipps on how to migrate from [Octopress][octopress] to [Jekyll][jekyll]. 

#### Permalinks

Permalinks somehow defaults to ``/mycategory/2014/05/01/title``.  
Set ``permalink: /blog/:year/:month/:day/:title`` in ``_config.yml`` to use a fixed prefix.

#### XML-Sitemap

There is a plugin to generate a ``sitemap.xml`` - <https://github.com/kinnetica/jekyll-plugins>

#### robots.txt  

The ``robots.txt`` can easily be adopted from the Octopress installation.

{% highlight yaml %}
{% raw %}
---
layout: nil
---
User-agent: *
Disallow: 

Sitemap: {{ site.url }}/sitemap.xml 
{% endraw %}
{% endhighlight %}

Ensure that ``url: http://yoursite.com`` has been set in ``_config.yml``.

#### Provide Atom feed  

This ``atom.xml`` provides atom feed functionality.

{% highlight xml %}
{% raw %}
---
layout: nil
---
<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>{{ site.name }}</title>
  <link href="{{ site.url }}/atom.xml" rel="self"/>
  <link href="{{ site.url }}"/>
  <updated>{{site.time | date_to_xmlschema }}</updated>
  <id>{{ site.url }}</id>
  <author>
    <name>{{ site.author }}</name>
    <email></email>
  </author>
  {% for post in site.posts %}
  <entry>
    <title>{{ post.title }}</title>
    <link href="{{ site.url }}"/>
    <updated>{{post.date | date_to_xmlschema }}</updated>
    <id>{{ site.url }}{{ post.url }}</id>
    <content type="html">{{ post.content | xml_escape }}</content>
  </entry>
  {% endfor %}
</feed>
{% endraw %}
{% endhighlight %}

As mentioned above, ``url: http://yoursite.com`` and ``author: Your Name`` must be set in ``_config.yml``.


#### Linking previous/next posts

Append this to ``_layouts/post.html`` for linking previous/next posts:

{% highlight html %}
{% raw %}
{% if page.previous %}
	<p><a href="{{ page.previous.url }}">« {{ page.previous.title }}</a></p>
{% endif %}
{% if page.next %}
	<p><a href="{{ page.next.url }}">{{ page.next.title }} »</a></p>
{% endif %}
{% endraw %}
{% endhighlight %}

Other useful variables can be found here: <http://jekyllrb.com/docs/variables/>.




[octopress]: http://octopress.org
[jekyll]:    http://jekyllrb.com