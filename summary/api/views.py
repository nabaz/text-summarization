from django.shortcuts import render
import bs4 as bs  
import urllib.request  
import re
import nltk
import heapq  
from django.http import HttpResponse
from .forms import UrlForm


def home(request):
    summary = ""
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UrlForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            scraped_data = urllib.request.urlopen(form.cleaned_data['url'])
            number_sentence = form.cleaned_data['summary_sentence'] or 10
            article = scraped_data.read()
            parsed_article = bs.BeautifulSoup(article,'lxml')
            paragraphs = parsed_article.find_all('p')

            article_text = ""

            for p in paragraphs:  
                article_text += p.text

                article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)  
                article_text = re.sub(r'\s+', ' ', article_text)  
                formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )  
                formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)  
                sentence_list = nltk.sent_tokenize(article_text)  

                stopwords = nltk.corpus.stopwords.words('english')

            word_frequencies = {}  
            for word in nltk.word_tokenize(formatted_article_text):  
                
                if word not in stopwords:
                    if word not in word_frequencies.keys():
                        word_frequencies[word] = 1
                    else:
                        word_frequencies[word] += 1
                    

            maximum_frequncy = max(word_frequencies.values())
            for word in word_frequencies.keys():  
                word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)


            sentence_scores = {}  
            for sent in sentence_list:  
                for word in nltk.word_tokenize(sent.lower()):
                    if word in word_frequencies.keys():
                        if len(sent.split(' ')) < 30:
                            if sent not in sentence_scores.keys():
                                sentence_scores[sent] = word_frequencies[word]
                            else:
                                sentence_scores[sent] += word_frequencies[word]




            summary_sentences = heapq.nlargest(number_sentence, sentence_scores, key=sentence_scores.get)

            summary = ' '.join(summary_sentences)  
            return render(request, 'url.html', {'summary' : summary})
    # if a GET (or any other method) we'll create a blank form
    else:
        form = UrlForm()
    
        return render(request, 'url.html', {'summary' : summary})  

    return render(request, 'url.html', {'summary' : summary}) 