from main import *


examples = [
"I am a student . I love ",
"I am a student . I live in America . I love ",
"I am a student . I live in America . I do not love money . I love ",
]


examples = [
# 190: The city 's growth has reflected the push and pull of many social and economic factors .
"The city 's growth has reflected the push and pull of many social and ",
# 299: Lewis McAllister , a businessman in Tuscaloosa , Alabama , was the first Republican to serve in the Mississippi House of Representatives since Reconstruction , 1962 @-@ 1968 ; he resided in Meridian prior to 1971 .
"Lewis McAllister , a businessman in Tuscaloosa , Alabama , was the first Republican to serve in the Mississippi House of",
# 735: The secrecy surrounding the circumstance of his death caused speculation for several days .
"The secrecy surrounding the circumstance of his death caused speculation for",
# 1014: The film was released on 3 February 2012 in the United States and Canada , and was released on 10 February in the UK .
"The film was released on 3 February 2012 in the United States and Canada , and was released",
# 1669: That court , noting Hubbard 's instruction that Scientologists should make money , make more money – make other people produce so as to make more money .
"That court , noting Hubbard 's instruction that Scientologists should make money , make more money – make other people produce so as to",
# 1701: Given the history of Nazism 's rise to power in Germany in the 1930s , the present German state has committed itself to taking active steps to prevent the rise of any ideology that threatens the values enshrined in the German constitution .
"Given the history of Nazism 's rise to power in Germany in the 1930s , the present German state has committed itself to taking active steps to prevent the rise of any ideology that threatens the values enshrined in",
# 2240: Sonic the Hedgehog is a platform video game developed by Sonic Team and published by Sega for the Sega Genesis console .
"Sonic the Hedgehog is a platform video game developed by Sonic Team and published by Sega for",
# 2547: During the tour , several bits and performances were filmed and later edited into a VHS and DVD entitled Around the World .
"During the tour , several bits and performances were filmed and later edited into a VHS and DVD entitled Around",
# 2853: Australia entered the Second World War on 3 September 1939 .
"Australia entered the Second World War on",
# 3167: Fort Scott National Historic Site is a historical area under the control of the United States National Park Service in Bourbon County , Kansas , United States .
"Fort Scott National Historic Site is a historical area under the control of the United States National Park Service in Bourbon County , Kansas ,"]


if __name__ == "__main__":

    vocabulary = data_loader.vocabulary
    for example in examples:
        print("*" * 100)
        preds, probabilitys = predict(example, pred_length=8, size_beam=10)
        for i in range(1):
            pred = preds[i].cpu().numpy()
            print("pred %d :" % (i + 1))
            for token in pred:
                print(vocabulary[token], end=' ')
            print()
