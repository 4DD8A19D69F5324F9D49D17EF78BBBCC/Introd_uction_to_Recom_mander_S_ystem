package edu.umn.cs.recsys.uu;

import org.grouplens.lenskit.basic.AbstractItemScorer;
import org.grouplens.lenskit.data.dao.ItemEventDAO;
import org.grouplens.lenskit.data.dao.UserEventDAO;
import org.grouplens.lenskit.data.event.Rating;
import org.grouplens.lenskit.data.history.History;
import org.grouplens.lenskit.data.history.RatingVectorUserHistorySummarizer;
import org.grouplens.lenskit.data.history.UserHistory;
import org.grouplens.lenskit.vectors.MutableSparseVector;
import org.grouplens.lenskit.vectors.SparseVector;
import org.grouplens.lenskit.vectors.VectorEntry;
import org.grouplens.lenskit.vectors.similarity.CosineVectorSimilarity;


import java.util.*;
import javax.annotation.Nonnull;
import javax.inject.Inject;

/**
 * User-user item scorer.
 * @author <a href="http://www.grouplens.org">GroupLens Research</a>
 */
public class SimpleUserUserItemScorer extends AbstractItemScorer {
    private final UserEventDAO userDao;
    private final ItemEventDAO itemDao;

    @Inject
    public SimpleUserUserItemScorer(UserEventDAO udao, ItemEventDAO idao) {
        userDao = udao;
        itemDao = idao;
    }

    @Override
    public void score(long user, @Nonnull MutableSparseVector scores) {
        SparseVector userVector = getUserRatingVector(user);

        // TODO Score items for this user using user-user collaborative filtering



        // This is the loop structure to iterate over items to score
        for (VectorEntry e: scores.fast(VectorEntry.State.EITHER)) {
            long itemid = e.getKey();

            //Weird method to get the top30   Please Ignore
            TreeMap<Double, Long> simMap = new TreeMap<Double, Long>();
            for (long uid: itemDao.getUsersForItem(itemid)){
                if (user != uid){
                    simMap.put(-getUserUserSimilarity(user,uid),uid);
                }
            }
            int counter=0;
            double simscore = 0.0;
            double simsum = 0.0;

            for(Map.Entry<Double,Long> ent:simMap.entrySet()){
                double sim = -ent.getKey();
                long userid = ent.getValue();

                simsum+=Math.abs(sim);
                simscore+= sim* (getUserRatingVector(userid).get(itemid)- getUserRatingVector(userid).mean());
                counter++;
                if(counter>=30) break;
            }

            double result = simscore / simsum +userVector.mean();
            scores.set(e,result);


        }
    }

    /**
     * Get the cosine similarity between user-user
     * @param user1  user ID 1
     * @param user2  user ID 2
     * @return  the cosine similarity
     */
    private double getUserUserSimilarity(long user1, long user2){
        CosineVectorSimilarity csim = new CosineVectorSimilarity();
        SparseVector uv1 = getUserRatingVector(user1);
        SparseVector uv2 = getUserRatingVector(user2);

        MutableSparseVector mv1  = uv1.mutableCopy();
        MutableSparseVector mv2  = uv2.mutableCopy();
        mv1.add(-uv1.mean());
        mv2.add(-uv2.mean());
        return csim.similarity(mv1,mv2);
    }



    /**
     * Get a user's rating vector.
     * @param user The user ID.
     * @return The rating vector.
     */
    private SparseVector getUserRatingVector(long user) {
        UserHistory<Rating> history = userDao.getEventsForUser(user, Rating.class);
        if (history == null) {
            history = History.forUser(user);
        }
        return RatingVectorUserHistorySummarizer.makeRatingVector(history);
    }
}
