/**
 * Created by scott on 9/14/17.
 */
$(document).ready(function(){
    var geneQueryString = "grouped_aggregate(filter(grouped_aggregate(apply(apply(cross_join(cross_join(filter(SSC.DataI,(VCF_GT='1/0' OR VCF_GT='0/1' OR VCF_GT='1/1') AND VCF_DP > 10 AND VCF_CQ > 50) as x,filter(SSC.VariantsI,Gene_refGene= 'GENE_NAME_PLACEHOLDER' AND VCF_FILTER='PASS') as y,x.Variant_ID,y.Variant_ID) as x1,SSC.MetaDataI as y1,x1.Individual_ID,y1.Individual_ID),Family,int64(Family_ID),Member,int64(dim_status(Status))),counter,iif ( status_dim ( Member ) = 'p1', 1, 2 )),SUM( counter ) AS family_pattern, MIN ( VarID ) AS VarID,Family, Variant_ID, Gene_refGene),family_pattern = 1),COUNT(*) AS num_variants, MIN ( VarID ) AS VarID,Family, Gene_refGene)";

    var geneInput = $("#gene-names");
    var geneInputWrapper = $("#gene-names-wrapper");
    var geneName = $("#gene-query");
    var geneAflQuery = null;

    geneName.text(geneQueryString);

    var geneAfl = "uniq(sort(project(SSC.VariantsI, Gene_refGene)))";
    if (!localStorage["geneData"]) {
      $.ajax({
        type: "POST",
        url: "/gene-data",
        data: {"query": geneAfl},
        success: (function (data) {
          localStorage["geneData"]=JSON.stringify(data["gene_names"]);
          geneInput.typeahead({ source:data["gene_names"], autoSelect: true });
          $("#gene-spinner").hide();
        }),
        dataType: "json"
      });
    }
    else {
      $("#gene-spinner").hide();
      geneInput.typeahead({ source:JSON.parse(localStorage["geneData"]), autoSelect: true });
    }


    geneInputWrapper.keyup(function() {
      var gene_name = geneInput.val();
      if (gene_name) {
        geneAflQuery = geneQueryString.replace(/GENE_NAME_PLACEHOLDER/, gene_name);
        geneName.text(geneQueryString.replace(/GENE_NAME_PLACEHOLDER/, gene_name));
      }
      else {
        geneAflQuery = geneQueryString;
        geneName.text(geneQueryString);
      }
    });
    geneInputWrapper.keydown(function() {
      var gene_name = geneInput.val();
       if (gene_name) {
        geneAflQuery = geneQueryString.replace(/GENE_NAME_PLACEHOLDER/, gene_name);
        geneName.text(geneQueryString.replace(/GENE_NAME_PLACEHOLDER/, gene_name));
      }
      else {
        geneAflQuery = geneQueryString;
        geneName.text(geneQueryString);
      }
    });


    $("#submit-afl-1").click(function(e){
        // Prevent default form submission behavior of a page reload
        e.preventDefault();

        // Gather values set in form
        var aflQuery = geneAflQuery;
        console.log(aflQuery);
        window.location.replace('/afl-table-no-limit?query='+ aflQuery);
    });
    $("#submit-afl-2").click(function(e){
        // Prevent default form submission behavior of a page reload
        e.preventDefault();

        // Gather values set in form
        var aflQuery = $("#afl-input").val();
        console.log(aflQuery);
        window.location.replace('/afl-table?query='+ aflQuery);
    });
    $("#submit-json").click(function(e){
        // Prevent default form submission behavior of a page reload
        e.preventDefault();

        // Gather values set in form
        var jsonQuery = $("#json-input").val();
        console.log(jsonQuery);
        window.location.replace('/json-table?query='+ jsonQuery);
    });
});
