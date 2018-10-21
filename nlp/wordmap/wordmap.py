import spacy
from spacy.tokens import Doc

SIMILARITY_TRESHOLD = 0.7

# lilo
# other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
# with nlp.disable_pipes(*other_pipes):  # only train NER


class Cluster(object):
    def __init__(self, item=None):
        if item:
            self.leader = item
            self.items = set([item])
        else:
            self.leader = None
            self.items = set([])

    def add(self, item):
        self.items.add(item)
        if (not self.leader):
            self.leader = item

    @staticmethod
    def merge(c1, c2):
        if not isinstance(c1, Cluster) or not isinstance(c2, Cluster):
            raise Exception()
        c = Cluster()
        c.items = c1.items.union(c2.items)
        c.leader = Cluster.select_leader(c1.leader, c2.leader)
        return c

    @staticmethod
    def select_leader(c1, c2):
        # lilo:TODO
        if not c1.leader:
            return c2.leader
        if not c2.leader:
            return c1.leader
        if (len(c1.leader) >= len(c2.leader)):
            return c1.leader
        return c2.leader


class Wordmap(object):
    def __init__(self, text, nlp):
        self.create_wordmap(text, nlp)

    def create_wordmap(self, text, nlp):
        self.nlp = nlp
        self.words = []
        with nlp.disable_pipes('nlpy_relations'):
            doc = nlp(text)
            clusters = self.cluster_entity_instances(doc)
            sorted(clusters, key=lambda c: len(c.items), reverse=True)
            print(clusters)  # lilo

    def cluster_entity_instances(self, doc):
        '''
        cluster instances of entities together
        '''
        # lilo:TODO
        # if (not 'instances' in doc._):
        #     Doc.set_extension('instances', default=[])

        # start with each entity in its own cluster
        clusters = []
        for e in doc.ents:
            clusters.append(Cluster(e))
        clusters = self.cluster(clusters)
        return clusters

    def cluster(self, clusters):
        if not clusters or len(clusters) < 2:
            print('lilo -----------------------')
            return clusters

        merge_occured = False
        new_clusters = []
        for c1 in clusters:
            c1_merged = False
            for c2 in clusters:
                if (c1 == c2):
                    continue
                if self.should_merge(c1, c2):
                    new_clusters.append(Cluster.merge(c1, c2))
                    c1_merged = True
                    break
            if c1_merged:
                merge_occured = True
            else:
                new_clusters.append(c1)
        if merge_occured:
            return self.cluster(new_clusters)  # recurse here
        return clusters

    def should_merge(self, c1, c2):
        if (c1.leader.label != c2.leader.label):
            return False
        # lilo:TODO - check leader entities similarity
        span1 = c1.leader
        span2 = c2.leader
        sim = span1.similarity(span2)
        if (sim < SIMILARITY_TRESHOLD):
            return False
        return True
