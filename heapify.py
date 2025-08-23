# import subprocess

# js_code = """
# function getData(dataid, getNextData, delay) {
#     setTimeout(() => {
#         console.log("Data", dataid);
#         if (getNextData) {
#             getNextData();
#         }
#     }, delay);
# }

# function run() {
#     getData(1, () => {
#         console.log("getting data 1----");
#         getData(2, () => {
#             console.log("getting data 2-----");
#         }, 8000);
#     }, 2000);
# }

# run();
# """

# # Start Node.js as a subprocess
# process = subprocess.Popen(
#     ["node", "-e", js_code],
#     stdout=subprocess.PIPE,
#     stderr=subprocess.PIPE,
#     text=True
# )

# # Read Node.js output line by line
# for line in process.stdout:
#     print(line, end="")








# )

# # print("Output from JS:", result.stdout)

# import execjs
# # JavaScript code\
# js_code = """
# function getData(dataid,getNextData)
# {
#      let messages = ["Data " + dataid];
#      if(getNextData)
#      {
#         getNextData();
#         }
#   }


# function run()
#           {   getData(1,()=>
# {
#   getData(2,()=>
#   { 

#   });
# });
# }
# """

# # Compile and run
# ctx = execjs.compile(js_code)
# result=ctx.call("run")
# print(result)




import heapq