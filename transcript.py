class Transcript:
    def __init__(self, filename, chunk_size=40, stride=10):
        self.filename = filename
        with open(filename, 'r') as f:
            self.transcript = [x for x in f.readlines() if x.strip() != '']
        self.transcript_chunks = self.create_chunks(chunk_size, stride)

    def create_chunks(self, chunk_size, stride):
        chunks = []
        for i in range(0, len(self.transcript), stride):
            chunks.append({'start': i, 'end': min(len(self.transcript), i + chunk_size)})
            if i + chunk_size >= len(self.transcript):
                break
        return chunks
