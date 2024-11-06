import pandas as pd
import time
from PIL import *
from os import walk, path
import subprocess
import time
import hashlib
from collections import defaultdict

def timeit(method):
    

    def timed(*args, **kw):
        time_start = time.time()
        result = method(*args, **kw)
        time_end = time.time()
        print((time_end - time_start) * 1000)
        return result

    return timed


class DuplicateFinder:
    

    def __init__(self, video_dir, recursive=False):
        
        super().__init__()

        if not isinstance(video_dir, str):
            raise TypeError("Argument videoDir must be a string!")
        self.video_dir = video_dir

        if not isinstance(recursive, bool):
            raise TypeError("Optional argument Recursive must be a Boolean!")
        self.recursive = recursive

        
        self.types = ["jpg", "jpeg", "JPEG", "JPG", "mp4", "mov", "webm" , "png"]

       
        self.videos_list = []

        
        self.buckets = []

    def generate_videos_list(self):
       
        videos_list = []
        for (dirpath, _, filenames) in walk(self.video_dir):
            videos = [
                path.join(dirpath, f)
                for f in filenames
                if f.split(".")[-1] in self.types
            ]
            videos_list.extend(videos)
            if not self.recursive:
                break
        return videos_list

    def get_duration(self, _video_path):
       
        result = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                _video_path,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=True,
        )
        return float(result.stdout)

    def chunk_reader(self, fobj, chunk_size=1024):
        
        while True:
            chunk = fobj.read(chunk_size)
            if not chunk:
                return
            yield chunk

    def get_hash(self, filename, first_chunk_only=False, hash_algo=hashlib.sha1):
       
        hashobj = hash_algo()
        with open(filename, "rb") as _f:
            if first_chunk_only:
                hashobj.update(_f.read(1024))
            else:
                for chunk in self.chunk_reader(_f):
                    hashobj.update(chunk)
        return hashobj.digest()

    def pure_dups(self):
       
        files_by_size = defaultdict(list)
        files_by_small_hash = defaultdict(list)
        files_by_full_hash = dict()

        for full_path in self.videos_list:
            try:
               
                full_path = path.realpath(full_path)
                file_size = path.getsize(full_path)
            except OSError:
               
                continue
            files_by_size[file_size].append(full_path)

       
        for size, files in files_by_size.items():
            if len(files) < 2:
                continue  

            for filename in files:
                try:
                    small_hash = self.get_hash(filename, first_chunk_only=True)
                except OSError:
               
                    continue
                files_by_small_hash[(size, small_hash)].append(filename)

       
        for files in files_by_small_hash.values():
            if len(files) < 2:
              
                continue

            for filename in files:
                try:
                    full_hash = self.get_hash(filename, first_chunk_only=False)
                except OSError:
                   
                    continue

                if full_hash in files_by_full_hash:
                    files_by_full_hash[full_hash].append(filename)
                else:
                    files_by_full_hash[full_hash] = [filename]

        dups = [items for items in files_by_full_hash.values() if len(items) > 1]
        self.buckets = dups

    def advanced_dups(self):
        
        raise NotImplementedError

    def find_dups(self):
        
        self.videos_list = self.generate_videos_list()

       
        self.pure_dups()

     
        flattened_dups = []
        for bucket in self.buckets:
            for filepath in bucket[1:]:
                flattened_dups.append(filepath)
        def to_keep(filepath):
            return filepath not in flattened_dups
        self.videos_list = list(filter(to_keep, self.videos_list))


   

    def get_results(self):
       
        dup_buckets = [bucket for bucket in self.buckets if len(bucket) > 1]
        deep_dup_len = sum([len(buckets) for buckets in dup_buckets])
        copyCount = deep_dup_len-len(dup_buckets)

            
        return dup_buckets , copyCount


def callDuplicateFinder(filename):
    print(filename)
    DUPLICATE_FINDER = DuplicateFinder(filename, True)
    DUPLICATE_FINDER.find_dups()
    x , copyCount = DUPLICATE_FINDER.get_results() 
            
    sub_str = "_"
    
    image_list = [] 
        
    return x,copyCount



