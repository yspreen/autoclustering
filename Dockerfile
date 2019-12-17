FROM r-base

LABEL input_1="nbclust_method,,,content" \
    input_2="nbclust_distance,,,content" \
    input_3="nbclust_index,,,content" \
    input_4="*" \
    output="*,,"

RUN mkdir /app \
    && cd /app \
    && echo 'install.packages("NbClust", repos="http://cran.r-project.org")' > setup.R \
    && Rscript setup.R

WORKDIR /app
ADD nbclust.R /app

ENTRYPOINT [ "Rscript" ]
CMD [ "/app/nbclust.R" ]
